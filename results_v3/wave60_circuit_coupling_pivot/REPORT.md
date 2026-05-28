# Wave60 Circuit-Coupling Pivot

Random seed: `20260527`.

## Verdict

No predictor satisfied the full circuit reopener gate. Donor-level circuit coupling can nominate candidate programs, but the available local package still lacks aligned MS anchoring and real perturbation/model evidence for a promotable circuit.

Operationalization:

- Build donor-level module and gene tables from local h5ad analyses.
- Standardize every predictor within each tissue/disease analysis.
- Define a pathogenic core as the mean of lipid-loader, lysosomal, HLA-II/APC, and MIF/CD74 modules.
- Residualize the pathogenic core against `ifn_apc` and `inflammatory_nfkb` within each analysis.
- Test Spearman coupling between each predictor and the residual pathogenic core within case donors only.
- Require cross-disease sign robustness before reopening any branch.

## Top Predictors

| predictor | call | diseases | combined FDR | positive fraction | up diseases | MS anchor | perturb/model hint |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| gene:FCGR2B | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.000887 | 0.73 | 1 | False | False |
| gene:GPNMB | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.00209 | 1.00 | 0 | True | False |
| gene:CCL20 | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.0024 | 0.65 | 4 | False | False |
| gene:P4HB | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.00501 | 0.65 | 3 | False | False |
| gene:PIKFYVE | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.00682 | 0.76 | 1 | False | False |
| gene:RAB3D | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.00694 | 0.65 | 1 | False | False |
| gene:APOL1 | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.0186 | 0.65 | 3 | False | False |
| gene:ACSL1 | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.0369 | 0.59 | 2 | False | False |
| gene:TGM2 | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.039 | 0.65 | 3 | False | False |
| gene:CSTA | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.0446 | 0.59 | 2 | False | False |
| gene:SPP1 | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.0481 | 0.75 | 1 | False | False |
| gene:AGRN | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.0635 | 0.59 | 3 | False | False |
| gene:JAK3 | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.0722 | 0.62 | 3 | True | False |
| gene:POMP | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.0777 | 0.59 | 4 | False | False |
| gene:PPARG | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.0794 | 0.69 | 1 | True | False |
| gene:CDV3 | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.0825 | 0.41 | 2 | True | False |
| gene:TFE3 | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.094 | 0.65 | 1 | False | False |
| gene:HSP90B1 | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.0964 | 0.65 | 3 | True | False |
| gene:ANGPTL4 | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.103 | 0.53 | 3 | False | False |
| gene:CD300LF | NO_GO_CIRCUIT_COUPLING_PIVOT | 5 | 0.108 | 0.69 | 2 | False | False |

## Interpretation

A strong circuit-coupling result alone is deliberately insufficient. It can still reflect donor severity, cell composition, or residual generic inflammation. A Wave60 reopener needs coupling plus disease recurrence, MS support, and perturbation/model support before external therapeutic audit.

The output tables preserve the failed branches because those failures determine the next pivot.

## Traceable Outputs

- `circuit_predictor_rank.tsv`
- `circuit_context_correlations.tsv`
- `circuit_predictor_disease_contrasts.tsv`
- `circuit_gate_matrix.tsv`
- `summary.json`
