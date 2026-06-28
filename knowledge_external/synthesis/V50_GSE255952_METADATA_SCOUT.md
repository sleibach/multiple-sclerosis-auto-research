# V50 GSE255952 Metadata Scout

Status: metadata-only scout. This artifact records whether GSE255952 is a
usable future route for steroid-confounder panel grounding. It does not import
expression values, make biological claims, or validate the locked V22 rule.

Generated metadata summary:
`analysis/v50_gse255952_metadata_scout/GSE255952_metadata_summary_v50.json`.

Raw GEO SOFT metadata snapshot:
`analysis/v50_gse255952_metadata_scout/GSE255952_series_metadata_soft.txt`.

OpenGWAS status: not used.

## Metadata Summary

| field | value |
|---|---|
| GEO accession | `GSE255952` |
| public status | `Public on Feb 20 2024` |
| PubMed ID | `38749180` |
| platform | `GPL23126`, Clariom D human array |
| data type | expression profiling by array |
| sample count | `48` |
| cell compartments | CD19+ B cells and CD4+ T helper cells |
| sampling | paired before first and after last high-dose methylprednisolone administration |
| disease context | MS relapse therapy, not DMF treatment response |
| response labels in metadata | 19 relapse treatments, 13 improved functional systems and 6 did not |
| supplementary files | gene/exon workflow processed matrix locator plus RAW tar locator |

Source:
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE255952

## Safe Interpretation

GSE255952 is a strong future route for testing steroid-response and
cell-compartment confounder panels because it has paired pre/post high-dose
methylprednisolone samples, B-cell and T-helper-cell separation, and improvement
status in the metadata.

It is not a validation cohort for the locked V22 DMF APC/HLA-II scalar:

- treatment is methylprednisolone relapse therapy, not dimethyl fumarate;
- compartments are CD19+ B cells and CD4+ T helper cells, not whole PBMC DMF
  monitoring;
- expression values were not imported in V50;
- no V22 module score or threshold was run.

## Future Grounding Route

If a future non-discovery validation or method-characterization task imports the
data, the allowed route is:

1. Download the processed gene-level matrix and sample metadata from GEO.
2. Verify sample pairing, compartment labels, T0/T1 status, relapse-course
   grouping, and improvement labels.
3. Map gene identifiers to the V32 glucocorticoid/steroid panel only.
4. Test whether the V32 steroid panel captures the expected pre/post
   methylprednisolone shift in each compartment.
5. Report compartment-specific steroid-panel performance as method support for
   confounder scoring, not as evidence about MS treatment-response biology or
   the V22 scalar.

## Decision

Queue as a future non-OpenGWAS, non-Gafson, metadata-verified route for
steroid-confounder panel stress testing. Do not route it through the frozen
Gafson/V22 validation harness except as an external steroid-panel sanity check.
