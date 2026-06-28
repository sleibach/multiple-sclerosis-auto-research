# V50 GWAS Catalog Harmonization Route Result

Status: route result only. This artifact uses public GWAS Catalog rows already
captured by V50 and does not call OpenGWAS. It does not make a project-direction
genetics conclusion, promote a target, or alter any grounded finding.

## Inputs

- `analysis/v50_allele_harmonization_prep/allele_harmonization_prep.tsv`
- `knowledge_external/synthesis/V50_ALLELE_HARMONIZATION_PREP.md`
- `knowledge_external/synthesis/V50_NON_OPENGWAS_FUTURE_GROUNDING_QUEUE.md`

## Outputs

- `analysis/v50_gwas_catalog_harmonization_route/harmonization_route_result.tsv`
- `analysis/v50_gwas_catalog_harmonization_route/summary.json`

## Result

| metric | value |
|---|---:|
| rsids checked | `3` |
| source-reported cross-trait allele contrasts extractable | `2` |
| project-direction harmonized rows | `0` |
| project-direction conclusion allowed | `false` |
| OpenGWAS used | `false` |

## What Was Extractable

| rsid | source-reported extractable state | interpretation boundary |
|---|---|---|
| `rs1250550` | GWAS Catalog candidate rows report MS risk allele `A` and Crohn disease risk allele `G`. | Source-reported cross-trait contrast is available, but project-side strand/orientation and effect-convention mapping remain unresolved. |
| `rs4613763` | GWAS Catalog candidate rows report MS risk allele `G` and Crohn disease risk allele `C`. | Source-reported cross-trait contrast is available, but project-side strand/orientation and effect-convention mapping remain unresolved. |
| `rs7522462` | GWAS Catalog candidate row reports MS risk allele `G`. | Single-disease locus-context route only; no cross-disease direction contrast was established in this rsid output. |

## Stop Point

The route stops here. The V50 data are sufficient to prepare a source-reported
allele contrast table, but not sufficient to make a project-grounded direction
claim. The missing inputs are:

1. strand/orientation confirmation for each rsid;
2. project disease/eQTL effect-allele convention mapping;
3. phenotype-specific project direction table alignment;
4. explicit handling or exclusion of ambiguous GWAS Catalog rows with `?`
   reported allele;
5. a no-target-promotion statement for any future harmonized output.

## Decision

Use the route output as a future harmonization input. Do not cite the
source-reported allele contrasts as project-grounded direction evidence until a
separate committed harmonization analysis resolves the stop-point inputs.

## Provenance

Prepared on 2026-06-28 from V50 GWAS Catalog route outputs. This note is
navigation and future-grounding preparation only.
