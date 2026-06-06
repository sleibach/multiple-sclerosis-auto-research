# Wave68 GSE282122 Unrestricted Myeloid Gene Screen

Random seed: `20260527`.

## Data

- Input h5ad: `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`.
- Paired major-state units: `110` site/state rows before threshold filtering.
- Thresholded rows: `86`.
- Genes tested: `33075`.

## Verdict

- Calls: `{'DESCRIPTIVE_GENE_SIGNAL': 66137, 'PARK_GENETIC_PERTURBATION_INTERSECTION': 13}`.
- This is an unrestricted discovery screen. Any candidate must still pass druggability, prior-art, and independent cross-dataset validation.

## Top Integrated Rows

| state | gene | call | score | raw response FDR | adjusted FDR | paired FDR | wave62 score | genetics | druggable | blocker | posthoc blocker |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| DC | RGS14 | PARK_GENETIC_PERTURBATION_INTERSECTION | 5.83 | 1 | 0.0113 | 1 | 5.3 | True | False | False |  |
| DC | CD274 | PARK_GENETIC_PERTURBATION_INTERSECTION | 5.48 | 1 | 0.0243 | 1 | 2.96 | True | False | False |  |
| DC | LPP | PARK_GENETIC_PERTURBATION_INTERSECTION | 5.45 | 1 | nan | 0.451 | 3.78 | True | False | False |  |
| Mono_macro | ARHGAP31 | PARK_GENETIC_PERTURBATION_INTERSECTION | 5 | 0.589 | 0.00784 | 1 | 1.96 | True | False | False |  |
| DC | TNFSF15 | PARK_GENETIC_PERTURBATION_INTERSECTION | 4.95 | 1 | 0.0162 | 1 | 2.4 | True | False | False |  |
| Mono_macro | NCF1 | PARK_GENETIC_PERTURBATION_INTERSECTION | 4.87 | 1 | nan | 0.162 | 1.94 | True | False | False |  |
| DC | CD80 | PARK_GENETIC_PERTURBATION_INTERSECTION | 4.53 | 1 | 0.0316 | 1 | 1.98 | True | False | False |  |
| DC | FCGR2B | PARK_GENETIC_PERTURBATION_INTERSECTION | 4.42 | 1 | nan | 0.691 | 1.84 | True | False | False |  |
| DC | IL7R | PARK_GENETIC_PERTURBATION_INTERSECTION | 4.28 | 1 | 0.0255 | 1 | 6.45 | True | False | True |  |
| Mono_macro | STAT4 | PARK_GENETIC_PERTURBATION_INTERSECTION | 4.24 | 0.587 | 0.00784 | 1 | 4.38 | True | True | True |  |
| Mono_macro | TNFRSF9 | PARK_GENETIC_PERTURBATION_INTERSECTION | 4.01 | 1 | nan | 0.558 | 1.57 | True | False | False |  |
| DC | DCLRE1B | PARK_GENETIC_PERTURBATION_INTERSECTION | 3.87 | 1 | 0.0373 | 1 | 1.58 | True | False | False |  |
| Mono_macro | FCGR2A | PARK_GENETIC_PERTURBATION_INTERSECTION | 2.35 | 1 | nan | 0.589 | 2.41 | True | False | True |  |
| Mono_macro | LINC01857 | DESCRIPTIVE_GENE_SIGNAL | 8.26 | 0.598 | 0.0266 | 0.0233 | 0 | False | False | False |  |
| Mono_macro | ATOX1 | DESCRIPTIVE_GENE_SIGNAL | 7.28 | 1 | nan | 0.0075 | 0 | False | False | False |  |
| DC | ATOX1 | DESCRIPTIVE_GENE_SIGNAL | 7.26 | 1 | nan | 0.0198 | 0 | False | False | False |  |
| Mono_macro | IKBKE | DESCRIPTIVE_GENE_SIGNAL | 6.86 | 0.598 | 0.014 | 0.376 | 2.45 | False | False | False |  |
| Mono_macro | ERH | DESCRIPTIVE_GENE_SIGNAL | 6.73 | 0.742 | 0.0152 | 0.0505 | 0 | False | False | False |  |
| Mono_macro | MT-CYB | DESCRIPTIVE_GENE_SIGNAL | 6.73 | 1 | nan | 0.0214 | 0 | False | False | False |  |
| DC | EBI3 | DESCRIPTIVE_GENE_SIGNAL | 6.7 | 0.892 | 0.00672 | 0.707 | 0 | False | False | False |  |
| DC | EPCAM | DESCRIPTIVE_GENE_SIGNAL | 6.69 | 1 | nan | 0.0198 | 0 | False | False | False |  |
| Mono_macro | UBE2D1 | DESCRIPTIVE_GENE_SIGNAL | 6.37 | 0.406 | 0.00818 | 0.443 | 0 | False | False | False |  |
| Mono_macro | KRT18 | DESCRIPTIVE_GENE_SIGNAL | 6.36 | 0.736 | 0.0266 | 0.0804 | 0 | False | False | False |  |
| Mono_macro | MT-ATP6 | DESCRIPTIVE_GENE_SIGNAL | 6.32 | 0.937 | nan | 0.0505 | 0 | False | False | False |  |
| DC | IL32 | DESCRIPTIVE_GENE_SIGNAL | 6.14 | 1 | nan | 0.14 | 0 | False | False | False |  |
| Mono_macro | TNFRSF4 | DESCRIPTIVE_GENE_SIGNAL | 6.12 | 0.633 | 0.0223 | 0.158 | 0 | False | False | False |  |
| Mono_macro | MT-CO3 | DESCRIPTIVE_GENE_SIGNAL | 6.12 | 0.984 | nan | 0.0505 | 0 | False | False | False |  |
| Mono_macro | PIGR | DESCRIPTIVE_GENE_SIGNAL | 6.1 | 1 | nan | 0.0214 | 0 | False | False | False |  |
| Mono_macro | EHF | DESCRIPTIVE_GENE_SIGNAL | 6.1 | 0.148 | 0.00414 | 1 | 0 | False | False | False |  |
| Mono_macro | MRPL33 | DESCRIPTIVE_GENE_SIGNAL | 5.93 | 0.633 | 0.0127 | 0.246 | 0.564 | False | False | False |  |
| DC | GRN | DESCRIPTIVE_GENE_SIGNAL | 5.9 | 1 | 0.0381 | 0.451 | 0 | False | False | False |  |
| Mono_macro | GPX4 | DESCRIPTIVE_GENE_SIGNAL | 5.89 | 1 | nan | 0.0804 | 1.54 | False | False | False |  |
| Mono_macro | ELOB | DESCRIPTIVE_GENE_SIGNAL | 5.77 | 0.695 | 0.0232 | 0.187 | 0 | False | False | False |  |
| DC | ARNTL2 | DESCRIPTIVE_GENE_SIGNAL | 5.74 | 0.929 | 0.00838 | 0.762 | 0 | False | False | False |  |
| Mono_macro | GHRL | DESCRIPTIVE_GENE_SIGNAL | 5.7 | 0.967 | nan | 0.0804 | 0 | False | False | False |  |
| Mono_macro | CSTA | DESCRIPTIVE_GENE_SIGNAL | 5.66 | 0.633 | 0.0235 | 0.421 | 1.07 | False | False | False |  |
| Mono_macro | FABP2 | DESCRIPTIVE_GENE_SIGNAL | 5.66 | 1 | nan | 0.0804 | 0 | False | False | False |  |
| DC | PTMA | DESCRIPTIVE_GENE_SIGNAL | 5.64 | 1 | nan | 0.0328 | 0 | False | False | False |  |
| Mono_macro | DAG1 | DESCRIPTIVE_GENE_SIGNAL | 5.56 | 0.897 | nan | 0.0933 | 0 | False | False | False |  |
| DC | RELB | DESCRIPTIVE_GENE_SIGNAL | 5.55 | 1 | nan | 0.301 | 0 | False | False | False |  |

## Top Raw Remission-Response Rows

| state | gene | n | remission mean | nonremission mean | raw delta | raw p | raw FDR |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Mono_macro | EHF | 29 | 2.23 | -0.516 | 2.74 | 9.81e-06 | 0.148 |
| Mono_macro | CALCOCO2 | 29 | -0.562 | 0.228 | -0.79 | 1.66e-05 | 0.148 |
| Mono_macro | CLEC9A | 29 | 1.97 | -1.16 | 3.13 | 1.74e-05 | 0.148 |
| Mono_macro | SNX10 | 29 | -1.17 | 0.399 | -1.57 | 1.8e-05 | 0.148 |
| Mono_macro | H3F3A | 29 | -0.309 | 0.0747 | -0.384 | 4.38e-05 | 0.267 |
| Mono_macro | TRIB3 | 29 | -1.38 | 1.02 | -2.4 | 4.84e-05 | 0.267 |
| Mono_macro | SMPD2 | 29 | -1.87 | 0.378 | -2.25 | 6.21e-05 | 0.293 |
| Mono_macro | MAP3K7CL | 29 | -2.52 | 0.841 | -3.36 | 0.000102 | 0.396 |
| Mono_macro | CLEC12A | 29 | -1.24 | 0.549 | -1.79 | 0.000108 | 0.396 |
| Mono_macro | PDP2 | 29 | -1.25 | 0.444 | -1.69 | 0.000142 | 0.406 |
| Mono_macro | COLEC12 | 29 | -1.39 | 0.608 | -2 | 0.000153 | 0.406 |
| Mono_macro | SGTB | 29 | -1.26 | 0.339 | -1.6 | 0.000157 | 0.406 |
| Mono_macro | UBE2D1 | 29 | -0.761 | 0.0101 | -0.771 | 0.000161 | 0.406 |
| Mono_macro | RAPH1 | 29 | -1.22 | 0.996 | -2.22 | 0.000172 | 0.406 |
| Mono_macro | LINC00482 | 29 | -0.394 | 0.581 | -0.976 | 0.000198 | 0.415 |
| Mono_macro | SMIM25 | 29 | -1.6 | 0.532 | -2.13 | 0.000201 | 0.415 |
| Mono_macro | TAX1BP1 | 29 | -0.456 | 0.128 | -0.584 | 0.000224 | 0.428 |
| Mono_macro | MKKS | 29 | -1.67 | 0.3 | -1.97 | 0.000233 | 0.428 |
| Mono_macro | TRG-AS1 | 29 | -1.35 | 0.441 | -1.79 | 0.000251 | 0.438 |
| Mono_macro | CTSS | 29 | -0.427 | 0.233 | -0.66 | 0.000288 | 0.46 |
| Mono_macro | AC004812.2 | 29 | -1.64 | 0.458 | -2.1 | 0.000292 | 0.46 |
| Mono_macro | NCDN | 29 | -1.42 | 0.379 | -1.8 | 0.000336 | 0.505 |
| Mono_macro | LTC4S | 29 | 2.11 | -0.251 | 2.36 | 0.000352 | 0.507 |
| Mono_macro | HLA-DQB1 | 29 | 0.612 | -0.213 | 0.826 | 0.000379 | 0.522 |
| Mono_macro | PDE2A | 29 | -0.976 | 0.835 | -1.81 | 0.000429 | 0.56 |
| Mono_macro | CYP27B1 | 29 | -2.49 | 0.805 | -3.29 | 0.000452 | 0.56 |
| Mono_macro | LTA4H | 29 | -0.804 | 0.309 | -1.11 | 0.00047 | 0.56 |
| Mono_macro | TXNDC5 | 29 | -1.19 | 0.0618 | -1.26 | 0.000485 | 0.56 |
| Mono_macro | SERPINA1 | 29 | -1.03 | 0.552 | -1.58 | 0.000522 | 0.56 |
| Mono_macro | BASP1 | 29 | -1.02 | 0.064 | -1.08 | 0.000529 | 0.56 |

## Top Paired Pharmacodynamic Rows

| state | gene | n pairs | mean delta | p | FDR |
| --- | --- | ---: | ---: | ---: | ---: |
| Mono_macro | ATOX1 | 43 | -0.646 | 2.27e-07 | 0.0075 |
| DC | EPCAM | 43 | 1.79 | 1.01e-06 | 0.0198 |
| DC | ATOX1 | 43 | -0.53 | 1.2e-06 | 0.0198 |
| Mono_macro | MT-CYB | 43 | 0.357 | 1.44e-06 | 0.0214 |
| Mono_macro | PIGR | 43 | 1.3 | 1.94e-06 | 0.0214 |
| Mono_macro | LINC01857 | 43 | -1.87 | 2.82e-06 | 0.0233 |
| DC | KLF6 | 43 | -0.387 | 3.52e-06 | 0.0328 |
| DC | PTMA | 43 | -0.147 | 3.97e-06 | 0.0328 |
| Mono_macro | H2AFJ | 43 | -0.43 | 5.6e-06 | 0.037 |
| Mono_macro | MT-ATP6 | 43 | 0.343 | 9.41e-06 | 0.0505 |
| Mono_macro | MT-CO3 | 43 | 0.376 | 1.07e-05 | 0.0505 |
| Mono_macro | ERH | 43 | -0.376 | 1.22e-05 | 0.0505 |
| Mono_macro | FABP2 | 43 | 0.859 | 2.33e-05 | 0.0804 |
| Mono_macro | GPX4 | 43 | -0.36 | 2.48e-05 | 0.0804 |
| Mono_macro | GHRL | 43 | -1.14 | 3.07e-05 | 0.0804 |
| Mono_macro | MT-CO2 | 43 | 0.252 | 3.15e-05 | 0.0804 |
| Mono_macro | KRT18 | 43 | 1.44 | 3.16e-05 | 0.0804 |
| Mono_macro | MT-ND4 | 43 | 0.342 | 4.47e-05 | 0.0897 |
| Mono_macro | AGR2 | 43 | 1.4 | 4.61e-05 | 0.0897 |
| Mono_macro | BNC2 | 43 | 1.1 | 4.64e-05 | 0.0897 |
| Mono_macro | CYB5D1 | 43 | 0.856 | 4.9e-05 | 0.0897 |
| Mono_macro | PLA2G2D | 43 | -1.62 | 4.95e-05 | 0.0897 |
| Mono_macro | AMN | 43 | 1.05 | 5.43e-05 | 0.0897 |
| Mono_macro | TSPAN8 | 43 | 1.27 | 5.55e-05 | 0.0897 |
| Mono_macro | IQCK | 43 | -0.739 | 5.87e-05 | 0.0897 |
| Mono_macro | COX17 | 43 | -0.299 | 5.97e-05 | 0.0897 |
| Mono_macro | CACNB3 | 43 | 0.844 | 6.51e-05 | 0.0933 |
| Mono_macro | DAG1 | 43 | 1.01 | 7.01e-05 | 0.0933 |
| Mono_macro | COX7C | 43 | -0.242 | 7.51e-05 | 0.0933 |
| Mono_macro | KCTD12 | 43 | 0.364 | 7.61e-05 | 0.0933 |

## Interpretation Guardrails

- Remission-response tests are associative and post-treatment outcome-linked, not randomized target perturbations.
- Wave68 post-hoc blockers encode already-completed V3 audits so the unrestricted screen does not reopen candidates previously rejected on stronger evidence.
- Genes with HLA/MHC symbols are not straightforward drug targets even when statistically strong.
- Wave62 genetics intersection is target-resolution triage, not proof that changing the gene changes disease.
