# V50 GWAS Catalog Fetcher Validation

Status: synthesis/navigation only. This note validates the reusable V50 GWAS
Catalog fetcher against the earlier V50 routing TSV. It does not add biological
evidence, perform allele harmonization, or change any genetics finding.

Script:

- `scripts/v50_fetch_gwas_catalog_associations.py`

Validation inputs:

- Prior routing TSV:
  `analysis/v50_gwas_catalog_allele_routing/gwas_catalog_rsid_rows_v50.tsv`
- New fetcher TSV:
  `analysis/v50_gwas_catalog_fetcher/gwas_catalog_associations.tsv`

Validation outputs:

- `analysis/v50_gwas_catalog_fetcher_validation/summary.json`
- `analysis/v50_gwas_catalog_fetcher_validation/row_match_validation.tsv`
- `analysis/v50_gwas_catalog_fetcher_validation/extra_new_rows.tsv`

## Result

Pass.

| check | result |
|---|---:|
| prior rows | `12` |
| fetcher rows | `12` |
| matched prior rows | `12` |
| missing prior rows | `0` |
| extra fetcher rows | `0` |
| OpenGWAS used | `false` |

Matched key columns:

- `rsid`
- `traits`
- `risk_alleles`
- `or_per_copy`
- `beta`
- `pvalue`
- `risk_frequency`
- `source_url`

## Interpretation

The reusable fetcher reproduces the previously generated V50 GWAS Catalog
routing rows for:

- `rs1250550`
- `rs4613763`
- `rs7522462`

It also adds extra convenience columns in the new output (`beta_direction`,
`author_reported_genes`, `chromosome_locations`) for future review.

## Boundary

This validation proves only that the script reproduces the prior GWAS Catalog
API extraction. It does not:

- harmonize alleles;
- infer strand orientation;
- compare to project coloc/eQTL outputs;
- promote KIF21B, GPR25, PTGER4, or ZMIZ1 as targets;
- replace OpenGWAS-dependent workflows after token renewal.

The next legitimate step is the separate allele-harmonization checklist in
`knowledge_external/synthesis/V50_ALLELE_HARMONIZATION_CHECKLIST.md`.
