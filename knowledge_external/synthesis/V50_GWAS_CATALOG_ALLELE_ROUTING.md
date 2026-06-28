# V50 GWAS Catalog Allele Routing

Status: external-layer routing and API extraction only. This artifact documents
a non-OpenGWAS route for allele-direction follow-up on three V50 genetics rows.
It does not change any grounded genetics finding.

Generated extraction:
`analysis/v50_gwas_catalog_allele_routing/gwas_catalog_rsid_rows_v50.tsv`.

OpenGWAS status: not used. The OpenGWAS JWT is expired, so this route uses only
the EBI GWAS Catalog public REST API.

## API Extraction Summary

| rsid | rows returned | source URL | immediate interpretation |
|---|---:|---|---|
| `rs1250550` | `8` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs1250550&projection=associationBySnp | Contains multiple immune-disease rows. The specific MS row reports `rs1250550-A`; the Crohn row reports `rs1250550-G`. This is the non-OpenGWAS input for future ZMIZ1 allele-direction harmonization. |
| `rs4613763` | `2` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs4613763&projection=associationBySnp | Contains the PTGER4 same-rsid MS/Crohn contrast: Crohn `rs4613763-C`, MS `rs4613763-G`. This supports future harmonized transfer-caution checking. |
| `rs7522462` | `2` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs7522462&projection=associationBySnp | Contains the chr1 MS row `rs7522462-G` and an unrelated pharmacogenomic row. This supports locus-context routing, not causal-gene promotion. |

## Safe Routing Rules

1. Use the extracted TSV as an input manifest, not as a project conclusion.
2. For `rs1250550` and `rs4613763`, the next executable step is allele
   harmonization against the project's MS/Crohn direction framework. Required
   fields: rsid, disease, reported risk allele, effect size, effect direction,
   study/source row, and strand/orientation check.
3. For `rs7522462`, the next step is locus-context comparison only. The current
   GWAS Catalog row supports a real MS association, but it does not resolve
   KIF21B versus GPR25 causality or intervention direction.
4. Do not use these rows to reopen any target without direction-matched
   project-grounded evidence.
5. Do not use OpenGWAS until the expired token is renewed; this route remains
   independent of OpenGWAS.

## Per-Row Routing

| future task | input rsid | route | allowed output |
|---|---|---|---|
| ZMIZ1 allele-direction rerun | `rs1250550` | Harmonize MS `A` and Crohn `G` reported risk alleles against the project ZMIZ1 direction framework. | A rerunnable direction-consistency table; no target claim. |
| PTGER4 transfer-caution rerun | `rs4613763` | Harmonize Crohn `C` and MS `G` reported risk alleles against the PTGER4 closure logic. | A rerunnable transfer-caution table; no PTGER4 reactivation. |
| chr1 KIF21B/GPR25 locus-context check | `rs7522462` | Compare the MS row and author-reported/locus context against V19 chr1 interpretation. | Locus-support and ambiguity table; no causal-gene promotion. |

## What This Does Not Do

- It does not replace OpenGWAS for any downstream genetics work.
- It does not validate external rows as project evidence.
- It does not perform strand harmonization or LD-aware fine mapping.
- It does not alter the V37 scored findings.

The practical value is narrow but useful: while OpenGWAS is expired, the project
still has a documented, rerunnable, non-OpenGWAS route for the three V50
genetics follow-ups.
