# V50 Allele-Harmonization Preparation

Status: routing/synthesis only. This note summarizes preparation tables derived
from the validated GWAS Catalog fetcher output. It does not perform allele
harmonization, does not compare to project direction conventions, and does not
change any genetics finding.

Inputs:

- `analysis/v50_gwas_catalog_fetcher/gwas_catalog_associations.tsv`
- `knowledge_external/synthesis/V50_ALLELE_HARMONIZATION_CHECKLIST.md`
- `knowledge_external/synthesis/V50_GWAS_FETCHER_VALIDATION.md`

Outputs:

- `analysis/v50_allele_harmonization_prep/allele_harmonization_prep.tsv`
- `analysis/v50_allele_harmonization_prep/allele_harmonization_route_summary.tsv`
- `analysis/v50_allele_harmonization_prep/summary.json`

## Summary

| metric | value |
|---|---:|
| total rows | `12` |
| direction-input candidate rows | `5` |
| rows with missing or ambiguous reported allele | `5` |
| background rows | `2` |
| rows currently comparable to project direction | `0` |
| OpenGWAS used | `false` |

## Route Summary

| rsid | route | rows | candidate rows | ambiguous rows | current status |
|---|---|---:|---:|---:|---|
| `rs1250550` | ZMIZ1 MS/Crohn direction contrast | `8` | `2` | `4` | prep-ready, not harmonized |
| `rs4613763` | PTGER4 MS/Crohn transfer-caution contrast | `2` | `2` | `0` | prep-ready, not harmonized |
| `rs7522462` | chr1 KIF21B/GPR25 locus-context check | `2` | `1` | `1` | prep-ready, not harmonized |

## What Is Ready

The prep table has extracted the rows that can feed a future harmonization step:

- `rs1250550`: MS row has reported risk allele `A`; Crohn row has reported risk
  allele `G`.
- `rs4613763`: Crohn row has reported risk allele `C`; MS row has reported risk
  allele `G`.
- `rs7522462`: MS row has reported risk allele `G`, useful for locus-context
  routing but not a cross-disease direction contrast by itself.

## What Is Not Ready

No row is currently eligible for a project-direction conclusion because the
following checks are still missing:

1. strand/orientation confirmation;
2. project effect-allele convention mapping;
3. phenotype-specific project direction table alignment;
4. exclusion or separate handling of ambiguous reported-allele rows;
5. explicit no-target-promotion output for chr1, PTGER4, and ZMIZ1 routes.

## Decision

Use the prep table as an input manifest for a future allele-harmonization run.
Do not cite the extracted risk alleles as project-grounded direction evidence
until the full checklist has been executed and committed.
