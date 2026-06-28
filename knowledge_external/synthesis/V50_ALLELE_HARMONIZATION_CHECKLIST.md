# V50 Allele-Harmonization Checklist

Status: future checklist only. This file specifies the minimum steps required
before the V50 GWAS Catalog rsid routes can be treated as project-grounded
direction checks. It does not perform harmonization and does not change any
genetics finding.

Inputs:

- `knowledge_external/synthesis/V50_GWAS_CATALOG_ALLELE_ROUTING.md`
- `analysis/v50_gwas_catalog_allele_routing/gwas_catalog_rsid_rows_v50.tsv`

OpenGWAS status: expired and not used.

## Scope

| rsid | intended check | current route status |
|---|---|---|
| `rs1250550` | ZMIZ1 MS/Crohn allele-direction check | candidate for future allele-harmonized rerun |
| `rs4613763` | PTGER4 MS/Crohn transfer-caution check | candidate for future allele-harmonized rerun |
| `rs7522462` | chr1 KIF21B/GPR25 locus-context check | locus-context only; not causal-gene resolution |

## Required Fields Before Any Direction Claim

For each disease-row pair:

1. rsid.
2. phenotype/disease label.
3. reported risk allele.
4. effect size and direction.
5. p-value.
6. study/accession/source row.
7. reference genome build if available.
8. strand/orientation status.
9. whether the allele is ambiguous under complement mapping.
10. mapping to the project's original allele/direction convention.

## Harmonization Steps

1. Import the GWAS Catalog rsid rows from the saved V50 manifest or fresh public
   GWAS Catalog API query.
2. Filter to same-disease labels relevant to the project comparison:
   MS, Crohn disease, inflammatory bowel disease only where explicitly used.
3. Drop rows with unknown reported risk allele for the core direction test, but
   retain them in an appendix as incomplete context.
4. Standardize alleles to uppercase A/C/G/T.
5. Check whether either allele pair is strand-ambiguous.
6. Map reported risk allele to the project effect-direction convention.
7. Compare disease-pair direction only after both rows pass allele completeness
   and orientation checks.
8. Record all excluded rows and exclusion reasons.

## Per-Rsid Decision Rules

| rsid | pass condition | fail / caution condition |
|---|---|---|
| `rs1250550` | MS and Crohn rows have complete, harmonizable alleles and preserve opposite disease-direction assignment. | Any strand ambiguity, incomplete allele, or inconsistent direction moves the row to caution until manual review. |
| `rs4613763` | MS and Crohn rows have complete, harmonizable alleles and preserve the PTGER4 opposite-allele transfer-caution pattern. | Any same-direction result after harmonization triggers contradiction triage before interpretation. |
| `rs7522462` | MS row remains a real locus-context record; no claim is made about causal gene or target direction. | Any attempt to promote KIF21B or GPR25 from the row alone is rejected. |

## Required Output Of A Future Rerun

A valid future rerun should write:

- `analysis/.../gwas_catalog_harmonized_rows.tsv`
- `analysis/.../gwas_catalog_harmonization_exclusions.tsv`
- a short summary with:
  - rows imported;
  - rows included;
  - rows excluded;
  - rsid-level decision;
  - statement that OpenGWAS was or was not used;
  - statement that no target claim is made from external rows alone.

## Decision

This checklist lets future sessions move from V50 source-specific external
records to a controlled, rerunnable allele-direction check. Until that rerun
happens, the V50 records remain external corroborating context, not project
genetics evidence.
