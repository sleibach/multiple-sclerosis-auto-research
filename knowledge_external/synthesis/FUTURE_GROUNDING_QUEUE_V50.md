# V50 Future-Grounding Delta Queue

Status: external-layer routing only. This file converts V50 sharper external
records into future project-grounding tasks. It does not report new project
findings and does not alter grounded conclusions, locked rules, or
pre-registrations.

## Summary

- V50 sharper records routed: `18`
- immediate non-OpenGWAS executable routes: `3`
- routes blocked on validation/cohort data or source data access: `6`
- context-only records with no immediate grounding task: `9`
- OpenGWAS status: expired; no OpenGWAS-dependent route should run until token
  renewal.

## Grounding Queue

| id | priority | status | external record | class / marker | source | proposed grounding task | blocker / route |
|---|---|---|---|---|---|---|---|
| V50_FG_001 | high | queued | `claim.gwas_catalog.zmiz1_rs1250550_ms_crohn_opposite_alleles.2026-06-28` | `external-verifiable` / `NOT_PROJECT_GROUNDED` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs1250550&projection=associationBySnp | Import the two GWAS Catalog association rows, harmonize rs1250550 alleles, and compare with the project's ZMIZ1 MS/Crohn direction framework. | Executable without OpenGWAS using GWAS Catalog public API. |
| V50_FG_002 | high | queued | `claim.gwas_catalog.ptger4_rs4613763_ms_crohn_opposite_alleles.2026-06-28` | `external-verifiable` / `NOT_PROJECT_GROUNDED` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs4613763&projection=associationBySnp | Import the two GWAS Catalog association rows, harmonize rs4613763 alleles, and compare with the project's PTGER4 naive-transfer closure. | Executable without OpenGWAS using GWAS Catalog public API. |
| V50_FG_003 | high | queued | `claim.gwas_catalog.chr1_rs7522462_kif21b_gpr25_ms.2026-06-28` | `external-verifiable` / `NOT_PROJECT_GROUNDED` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs7522462&projection=associationBySnp | Import the GWAS Catalog row and compare author-reported genes plus genomic context against the V19 KIF21B/GPR25 causal-gene and hard-target interpretation. | Executable without OpenGWAS; do not promote any target without project-grounded direction and tractability. |
| V50_FG_004 | high | blocked_on_data | `claim.gafson_2018.dmf_pbmc_neda4_transcriptome_context.2026-06-28` | `external-verifiable` / `NOT_PROJECT_GROUNDED` | https://pmc.ncbi.nlm.nih.gov/articles/PMC6168332/ | Ingest only through the frozen V42/V44 harness and score the locked V22 scalar plus pre-specified confounders. | Blocked until authorized usable Gafson expression/label package is available; no scouting beyond quarantine rules. |
| V50_FG_005 | high | blocked_on_data | `claim.sanchez_sanz_2023.dmf_pbmc_response_signature_context.2026-06-28` | `external-verifiable` / `NOT_PROJECT_GROUNDED` | https://www.omicsdi.org/dataset/geo/GSE235357 | Check whether GSE235357 has paired baseline/early treatment, labels, and V22 module genes; if usable, route through the frozen harness or a pre-registered secondary validation. | Needs repository data retrieval and schema verification; do not count usable before paired structure, labels, and module genes are confirmed. |
| V50_FG_006 | medium | blocked_on_data | `claim.jcc_2024.crohn_pants_antitnf_interferon_modules.2026-06-28` | `external-verifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/37776235/ | If expression data are accessible, score project IFN/APC modules in PANTS blood data and test whether Crohn downstream response convergence reproduces. | Blocked on data access/locator review. |
| V50_FG_007 | medium | blocked_on_data | `claim.nat_immunol_2024.imid_antitnf_single_cell_atlas.2026-06-28` | `external-verifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/39438660/ | If single-cell data are accessible, map project IFN/APC and APC-axis modules across disease/treatment response layers. | Blocked on source data access and permitted reuse route. |
| V50_FG_008 | medium | blocked_on_data | `claim.biorxiv_2026.ebv_anti_cns_bcell_apc_ms_context.2026-06-28` | `external-verifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/41727017/ | If data become accessible and source status is acceptable, test EBV-linked anti-CNS B-cell APC state against project IFN/APC modules and autoimmune specificity controls. | Blocked on data access and preprint/source-status review. |
| V50_FG_009 | medium | queued_context_only | `claim.eji_2018.mif_cd74_bcell_ms_context.2026-06-28` | `external-verifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/30160778/ | Optional: score MIF/CD74/CXCR4 state in held B-cell layers, if already available, and compare with V26 coupled-axis loadings. | Executable only if a held B-cell layer with these genes is already indexed; otherwise data-limited. |

## Context-Only Records

The following V50 records are useful for interpretation but should not trigger a
standalone grounding task unless a specific same-definition dataset appears:

| record | source | reason |
|---|---|---|
| `claim.carlstrom_2019.dmf_monocyte_ros_response_context.2026-06-28` | https://www.nature.com/articles/s41467-019-11139-3 | Different DMF response biology and marker class than locked V22 scalar. |
| `claim.diebold_2022.dmf_high_dimensional_immune_monitoring_context.2026-06-28` | https://www.pnas.org/doi/10.1073/pnas.2205042119 | High-dimensional immune monitoring context, not the frozen transcriptomic scalar. |
| `claim.hmg_2019.zmiz1_dendritic_vitamin_d_context.2026-06-28` | https://academic.oup.com/hmg/article/28/2/269/5115479 | Mechanistic ZMIZ1 context, not direct MS/Crohn allele-direction test. |
| `claim.jmg_2010.kif21b_ms_susceptibility_replication.2026-06-28` | https://pubmed.ncbi.nlm.nih.gov/20587413/ | Susceptibility-locus context, not causal-gene or direction-matched target test. |
| `claim.iuphar.gpr25_orphan_gpcr_context.2026-06-28` | https://www.guidetopharmacology.org/services/targets?name=GPR25 | Tractability caution context, not disease causality. |
| `claim.ncbi_gene.cd74_mhc2_mif_molecular_context.2026-06-28` | https://www.ncbi.nlm.nih.gov/gene/972 | Molecular background for CD74 bridge, not MS validation. |
| `claim.jimmunol_2014.hla_dra1_cd74_mif_eae_context.2026-06-28` | https://pubmed.ncbi.nlm.nih.gov/24683185/ | Animal-model mechanistic context, not human MS validation. |
| `claim.nature_2022.ebna1_glialcam_crossreactive_bcells_ms.2026-06-28` | https://pubmed.ncbi.nlm.nih.gov/35073561/ | EBV-MS B-cell mechanism, not IFN/APC imprint specificity test. |
| `claim.plos_genet_2007.ptger4_crohn_expression_modulation.2026-06-28` | https://pubmed.ncbi.nlm.nih.gov/17447842/ | Crohn-side PTGER4 expression context, not MS transfer validation. |

## Operating Rules

1. External records never become evidence by being queued here.
2. Grounding tasks must use reachable data and project code, with null or
   sensitivity checks where predictive.
3. OpenGWAS-dependent refresh is disabled until the expired JWT is renewed.
4. Validation-facing DMF records enter only through frozen harnesses and
   quarantine rules.
