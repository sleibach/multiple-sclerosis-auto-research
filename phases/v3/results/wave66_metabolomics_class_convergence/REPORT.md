# Wave66 Metabolomics/Lipidomics Class Convergence

Random seed: `20260527`.

## Scope

This is an orthogonal biochemical audit of the cross-autoimmune lipid-lysosomal/APC hypothesis.
It does not claim a cell-intrinsic myeloid mechanism or therapeutic target by itself.

## Availability

| study | label | samples | factor rows | data status | data features | data samples |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| ST001949 | RA | 60 | 60 | downloaded | 649.0 | 60.0 |
| ST000899 | IBD | 60 | 60 | downloaded | 671.0 | 60.0 |
| ST002470 | UC | 89 | 89 | downloaded | 728.0 | 89.0 |
| ST002732 | SLE | 207 | 207 | downloaded | 144.0 | 207.0 |
| ST002949 | AS | 268 | 268 | downloaded | 26.0 | 240.0 |
| ST000422 | T1D | 180 | 180 | downloaded | 2125.0 | 180.0 |
| ST003328 | MS_model | 42 | 42 | downloaded | 642.0 | 42.0 |
| ST000298 | Psoriasis | 9 | 9 | downloaded | 9.0 | 9.0 |
| ST001636 | T1D_TEDDY_lipidomics | 11560 | 11560 | not_requested | nan | nan |
| ST001386 | T1D_TEDDY_metabolomics | 11560 | 0 | not_requested | nan | nan |

## Convergence Gate

- No biochemical class is promoted as a V3 therapeutic mechanism from Wave66 alone.

| class | call | tested diseases | same direction | supportive diseases | direction | median g | treatment/improvement normalizing hits |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: |
| amino_acid | DESCRIPTIVE_OR_WEAK | 5 | 4 | AS,Crohn,RA,UC | lower_in_case_or_worse | -0.729 | 1 |
| ceramide | DESCRIPTIVE_OR_WEAK | 6 | 5 | MS_model,RA,SLE | higher_in_case_or_worse | 0.712 | 1 |
| phosphatidylcholine | DESCRIPTIVE_OR_WEAK | 6 | 4 | AS,Crohn,UC | lower_in_case_or_worse | -0.357 | 2 |
| unclassified | DESCRIPTIVE_OR_WEAK | 7 | 4 | AS,MS_model,RA | higher_in_case_or_worse | 0.168 | 0 |
| glycosphingolipid | DESCRIPTIVE_OR_WEAK | 5 | 4 | MS_model,RA,UC | higher_in_case_or_worse | 0.64 | 0 |
| lysophosphatidylcholine | DESCRIPTIVE_OR_WEAK | 6 | 4 | MS_model,RA | higher_in_case_or_worse | 0.0968 | 1 |
| steroid | DESCRIPTIVE_OR_WEAK | 5 | 4 | Crohn,UC | lower_in_case_or_worse | -0.699 | 0 |
| phosphatidylglycerol | DESCRIPTIVE_OR_WEAK | 3 | 3 | MS_model,SLE | higher_in_case_or_worse | 0.433 | 1 |
| eicosanoid_oxylipin | DESCRIPTIVE_OR_WEAK | 5 | 3 | MS_model,RA | higher_in_case_or_worse | 0.256 | 0 |
| acylcarnitine | DESCRIPTIVE_OR_WEAK | 4 | 3 | Crohn,UC | lower_in_case_or_worse | -0.452 | 0 |
| phosphatidylethanolamine | DESCRIPTIVE_OR_WEAK | 6 | 3 | Crohn,MS_model | higher_in_case_or_worse | 0.00799 | 0 |
| fatty_acid | DESCRIPTIVE_OR_WEAK | 6 | 4 | RA | higher_in_case_or_worse | 0.174 | 1 |
| sphingomyelin | DESCRIPTIVE_OR_WEAK | 6 | 4 | MS_model | higher_in_case_or_worse | 0.22 | 0 |
| nicotinamide_nad | DESCRIPTIVE_OR_WEAK | 6 | 3 | AS | higher_in_case_or_worse | -0.328 | 1 |
| pyrimidine | DESCRIPTIVE_OR_WEAK | 4 | 3 | Crohn | lower_in_case_or_worse | -0.315 | 0 |
| phosphatidylinositol | DESCRIPTIVE_OR_WEAK | 6 | 3 | MS_model | higher_in_case_or_worse | -0.0257 | 0 |
| diacylglycerol | DESCRIPTIVE_OR_WEAK | 5 | 3 | MS_model | higher_in_case_or_worse | 0.0426 | 0 |
| purine | DESCRIPTIVE_OR_WEAK | 5 | 3 | AS | higher_in_case_or_worse | 0.0395 | 0 |
| sterol | DESCRIPTIVE_OR_WEAK | 4 | 2 | MS_model | higher_in_case_or_worse | -0.258 | 1 |
| cholesteryl_ester | DESCRIPTIVE_OR_WEAK | 3 | 2 | MS_model | higher_in_case_or_worse | 0.3 | 1 |

## Strongest Per-Contrast Class Rows

| study | disease | contrast | type | class | n features | g | p | FDR |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| ST002949 | AS | AS_vs_control | disease_control | acylcarnitine | 1 | 0.76 | 0.00017 | 0.000227 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | acylcarnitine | 4 | -1.31 | 0.000152 | 0.000436 |
| ST000899 | UC | UC_vs_control | disease_control | acylcarnitine | 4 | -0.847 | 0.00967 | 0.0645 |
| ST002949 | AS | AS_vs_control | disease_control | amino_acid | 3 | -1.14 | 1.1e-07 | 4.42e-07 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | amino_acid | 95 | -1.67 | 4.36e-06 | 1.45e-05 |
| ST001949 | RA | RA_vs_control | disease_control | amino_acid | 55 | -0.729 | 0.0244 | 0.0983 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | bile_acid | 19 | 1.29 | 0.000189 | 0.000473 |
| ST001949 | RA | RA_vs_control | disease_control | bile_acid | 3 | -0.681 | 0.0342 | 0.107 |
| ST000899 | UC | UC_vs_control | disease_control | bile_acid | 19 | -1.34 | 0.000154 | 0.00308 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | ceramide | 10 | 1.4 | 0.0171 | 0.0362 |
| ST001949 | RA | RA_vs_control | disease_control | ceramide | 17 | 0.959 | 0.00374 | 0.0357 |
| ST002732 | SLE | SLE_high_CAC_vs_null | severity_tissue_damage | ceramide | 39 | 0.793 | 0.0341 | 0.17 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | cholesteryl_ester | 30 | 3.36 | 7.4e-05 | 0.000468 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | diacylglycerol | 6 | -0.89 | 0.00724 | 0.0121 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | diacylglycerol | 29 | 1.23 | 0.0321 | 0.05 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | eicosanoid_oxylipin | 4 | 3.44 | 7.56e-08 | 1.44e-06 |
| ST001949 | RA | RA_vs_control | disease_control | eicosanoid_oxylipin | 4 | 0.933 | 0.00486 | 0.0357 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | fatty_acid | 12 | -1.95 | 2.41e-07 | 2.4e-06 |
| ST002470 | UC | UC_week0_modsev_vs_mild | severity | fatty_acid | 12 | -0.783 | 0.00408 | 0.0857 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | glycosphingolipid | 3 | 2.09 | 0.00196 | 0.0062 |
| ST001949 | RA | RA_vs_control | disease_control | glycosphingolipid | 8 | 0.64 | 0.0481 | 0.121 |
| ST000899 | UC | UC_vs_control | disease_control | glycosphingolipid | 3 | 0.878 | 0.00771 | 0.0645 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | lysophosphatidylcholine | 11 | 1.7 | 0.00709 | 0.0193 |
| ST001949 | RA | RA_vs_control | disease_control | lysophosphatidylcholine | 21 | 0.631 | 0.0493 | 0.121 |
| ST002949 | AS | AS_vs_control | disease_control | lysophosphatidylethanolamine | 1 | -0.737 | 0.000361 | 0.000413 |
| ST002949 | AS | AS_vs_control | disease_control | nicotinamide_nad | 1 | 1.97 | 2.75e-16 | 2.2e-15 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | nicotinamide_nad | 5 | -1.76 | 1.94e-06 | 7.77e-06 |
| ST001949 | RA | RA_vs_control | disease_control | nicotinamide_nad | 2 | -0.726 | 0.0268 | 0.0983 |
| ST002470 | UC | UC_week0_modsev_vs_mild | severity | nicotinamide_nad | 4 | -0.752 | 0.0283 | 0.198 |
| ST002949 | AS | AS_vs_control | disease_control | phosphatidylcholine | 2 | -0.943 | 3.95e-06 | 7.9e-06 |
| ST002732 | SLE | SLE_medhigh_CAC_vs_null | severity_tissue_damage | phosphatidylcholine | 23 | 0.589 | 0.000224 | 0.00224 |
| ST002732 | SLE | SLE_high_CAC_vs_null | severity_tissue_damage | phosphatidylcholine | 23 | 0.934 | 0.0039 | 0.039 |
| ST002470 | UC | UC_week0_modsev_vs_mild | severity | phosphatidylcholine | 52 | -0.681 | 0.0139 | 0.146 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | phosphatidylethanolamine | 13 | 1.23 | 0.0003 | 0.000666 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | phosphatidylglycerol | 24 | 1.63 | 0.0086 | 0.0204 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | phosphatidylinositol | 38 | 1.24 | 0.0342 | 0.05 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | phosphatidylserine | 27 | 1.34 | 0.0233 | 0.0442 |
| ST002949 | AS | AS_vs_control | disease_control | purine | 2 | 0.675 | 4.63e-07 | 1.23e-06 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | purine | 29 | -0.628 | 0.05 | 0.0769 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | pyrimidine | 11 | -1.93 | 3.61e-07 | 2.4e-06 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | sphingomyelin | 18 | -1.85 | 6.48e-07 | 3.24e-06 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | sphingomyelin | 21 | 1.22 | 0.0312 | 0.05 |
| ST000899 | UC | UC_vs_control | disease_control | sphingomyelin | 18 | -0.663 | 0.039 | 0.112 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | steroid | 20 | -0.902 | 0.0069 | 0.0121 |
| ST000899 | UC | UC_vs_control | disease_control | steroid | 20 | -0.699 | 0.0309 | 0.103 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | sterol | 1 | -1.22 | 0.000333 | 0.000666 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | sterol | 1 | 4.42 | 1.13e-05 | 0.000107 |
| ST000899 | UC | UC_vs_control | disease_control | sterol | 1 | -0.697 | 0.0305 | 0.103 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | triacylglycerol | 81 | 2.78 | 9.91e-05 | 0.000471 |
| ST001949 | RA | RA_vs_control | disease_control | triacylglycerol | 109 | -0.892 | 0.00656 | 0.0361 |
| ST002949 | AS | AS_vs_control | disease_control | unclassified | 15 | 0.57 | 1.45e-05 | 2.33e-05 |
| ST000899 | Crohn | Crohn_vs_control | disease_control | unclassified | 383 | -2.12 | 4.28e-08 | 8.56e-07 |
| ST003328 | MS_model | PMS_untreated_vs_AMC_untreated | disease_model | unclassified | 55 | 2.35 | 0.000804 | 0.00306 |
| ST000298 | Psoriasis | psoriasis_involved_vs_normal | disease_control | unclassified | 4 | -1.94 | 0.0484 | 0.0967 |
| ST001949 | RA | RA_vs_control | disease_control | unclassified | 232 | 0.997 | 0.00274 | 0.0357 |
| ST000899 | UC | UC_vs_control | disease_control | unclassified | 383 | -0.761 | 0.0188 | 0.0938 |

## Interpretation Guardrails

- Serum/plasma/cell-model metabolites do not establish tissue myeloid causality.
- Class labels are regex harmonizations from RefMet/metabolite names, not curated LIPID MAPS ontology calls.
- Treatment/improvement contrasts are unpaired unless the public metadata exposes pairing; they are direction checks only.
- TEDDY studies were not used for class effects because public Workbench factors lack direct endpoint labels here and `ST001636` returned no feature data from the REST `data` endpoint.
