# V50 Source-Independence Delta

Status: synthesis/navigation only. This note prevents V50 row counts from being
over-read as fully independent corroboration counts. It does not add evidence
or change any grounded finding.

Primary source: `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V50.md`.

## Summary

- V50 decision-relevant new convergence rows: `11`
- V50 row-specific canonical source URLs behind those rows: `11`
- V50 platform-level source families after conservative de-duplication: `9`
- V50 genuine contradiction rows: `0`
- V50 confounder-context records added in task 20: `6`
- V50 confounder-context source families: `6`

Interpretation: cite V50 as `11` source-specific convergence rows, but do not
call them `11` fully independent external sources. The most conservative
independence statement is:

> V50 adds `11` source-specific convergence rows backed by `9` platform-level
> source families, plus `6` treatment-response confounder context records that
> support validation guards but do not validate the locked V22 scalar.

## Decision-Relevant Convergence Source Clusters

| grounded finding | external record(s) | canonical source URL(s) | source-family accounting | interpretation |
|---|---|---|---|---|
| ZMIZ1 opposite-direction MS/Crohn decoupling | `claim.gwas_catalog.zmiz1_rs1250550_ms_crohn_opposite_alleles.2026-06-28` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs1250550&projection=associationBySnp | `shared_database_family`: GWAS Catalog | Row-specific support for ZMIZ1 direction, but not independent from other GWAS Catalog allele rows at the platform level. |
| chr1 KIF21B/GPR25 locus real but hard target | `claim.gwas_catalog.chr1_rs7522462_kif21b_gpr25_ms.2026-06-28`; `claim.jmg_2010.kif21b_ms_susceptibility_replication.2026-06-28` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs7522462&projection=associationBySnp; https://pubmed.ncbi.nlm.nih.gov/20587413/ | `mixed`: GWAS Catalog shared database plus independent paper | One database-family row plus one paper-family row. The locus is real; intervention-grade status remains unsupported. |
| GPR25 demotion | `claim.iuphar.gpr25_orphan_gpcr_context.2026-06-28` | https://www.guidetopharmacology.org/services/targets?name=GPR25 | `single_database_family`: IUPHAR | Independent target-class/tractability context; not disease causality. |
| Coupled APC remodeling architecture | `claim.eji_2018.mif_cd74_bcell_ms_context.2026-06-28`; `claim.ncbi_gene.cd74_mhc2_mif_molecular_context.2026-06-28`; `claim.jimmunol_2014.hla_dra1_cd74_mif_eae_context.2026-06-28` | https://pubmed.ncbi.nlm.nih.gov/30160778/; https://www.ncbi.nlm.nih.gov/gene/972; https://pubmed.ncbi.nlm.nih.gov/24683185/ | `three_source_families`: MS immune-cell paper, NCBI gene annotation, EAE mechanistic paper | Multiple source families support plausibility of the HLA-II/CD74/MIF bridge, but none externally validates the full V26 human axis. |
| Crohn downstream IFN/APC convergence | `claim.jcc_2024.crohn_pants_antitnf_interferon_modules.2026-06-28` | https://pubmed.ncbi.nlm.nih.gov/37776235/ | `single_paper_family` | Independent Crohn treatment-response context with prediction caveat. |
| Layer-specific autoimmune transfer-validity map | `claim.nat_immunol_2024.imid_antitnf_single_cell_atlas.2026-06-28` | https://pubmed.ncbi.nlm.nih.gov/39438660/ | `single_paper_family` | Independent cross-disease treatment-response atlas context. |
| PTGER4 naive-transfer closure | `claim.gwas_catalog.ptger4_rs4613763_ms_crohn_opposite_alleles.2026-06-28`; `claim.plos_genet_2007.ptger4_crohn_expression_modulation.2026-06-28` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs4613763&projection=associationBySnp; https://pubmed.ncbi.nlm.nih.gov/17447842/ | `mixed`: GWAS Catalog shared database plus independent paper | Same-rsid allele contrast plus Crohn-side regulatory context strengthen transfer caution, not target reactivation. |

## Confounder-Context Source Clusters

The task-20 records are not counted as V22 rule corroborations. They are counted
as validation-guard context.

| confounder class | external record(s) | canonical source URL(s) | source-family accounting | interpretation |
|---|---|---|---|---|
| Steroid / glucocorticoid transcriptome response | `claim.jneurol_2004.methylprednisolone_ms_immune_gene_suppression.2026-06-28`; `claim.cns_neurosci_ther_2024.glucocorticoid_resistance_ms_whole_blood.2026-06-28`; `claim.biopha_2024.methylprednisolone_b_t_cell_transcriptome_ms.2026-06-28` | https://link.springer.com/article/10.1007/s00415-004-0516-y; https://pmc.ncbi.nlm.nih.gov/articles/PMC10848073/; https://pubmed.ncbi.nlm.nih.gov/38749180/ | `three_source_families` | Supports steroid-response scoring as a validation guard; does not validate the V22 scalar. |
| DMF leukocyte / immune-cell composition | `claim.sci_rep_2018.dmf_persistent_immune_composition_ms.2026-06-28`; `claim.plos_one_2020.dmf_leukocyte_response_patient_factors_ms.2026-06-28`; `claim.mult_scler_2017.dmf_response_lymphocyte_subsets_ms.2026-06-28` | https://www.nature.com/articles/s41598-018-26519-w; https://pubmed.ncbi.nlm.nih.gov/32045436/; https://journals.sagepub.com/doi/10.1177/1352458517703799 | `three_source_families` | Supports composition diagnostics and deconvolution as validation guards; does not validate the V22 scalar. |

## Anti-Overcounting Rule

When summarizing V50:

- say `11 source-specific convergence rows backed by 9 platform-level source
  families`;
- do not say `11 independent external confirmations`;
- say `6 confounder-context records support validation guards`;
- do not say the confounder-context records externally validate the V32 adjusted
  result.

This preserves the asymmetry: external convergence raises confidence in the
context around a grounded finding; it does not become the evidence itself.
