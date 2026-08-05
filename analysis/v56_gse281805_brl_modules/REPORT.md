# V56 Donor-Level Broad-Rim-Lesion Module Test

## Verdict

**Frozen primary result: receptor_cd44_cxcr4, mif_ligand, lysosomal_unique, resolution_efferocytosis_proxy cleared the first association gate.**

**Overall interpretation: inconclusive for route advancement. No module clears the post-result common-slide sensitivity, and matched NAWM is absent from the processed deposit.**

This is a donor-aggregated reanalysis of a progression-associated postmortem lesion phenotype. It is not evidence that any intervention slows disability, and it does not establish a causal target.

## Cohort And Audit

- Source matrix: 120 quality-controlled lesion AOIs, 17 unique MS donors.
- Donor-state units: 22. Primary BRL donors: 8; mixed-rim donors: 7.
- Frozen-module coverage: 8/9 valid. Under-covered modules remain untestable and were not redefined.
- Raw GEO identity audit: 117/120 processed AOIs have a deposited DCC. The source workbook contains all 120, but raw reconstruction cannot exactly reproduce `DSP-1001660021304-C-H02;DSP-1001660021306-A-G06;DSP-1001660021306-A-G08`.
- Every primary p-value enumerates all donor-label assignments; max-T controls all valid frozen modules.
- NAWM expression was not present in the deposited processed matrix. The stronger matched-NAWM difference-of-differences is therefore blocked pending raw reconstruction and was not approximated.
- Synthetic method checks: vectorized exact engine versus independent naive enumeration = True; 1543/30000 null families passed at max-T <= 0.05 across three seeds (one-sided binomial p for excess over 0.05=0.1303); planted 4-SD max-T p-values were 0.0001554, 0.0001554, 0.0001554. Synthetic results characterize code behavior only, never MS biology.


## Untestable Frozen Modules

- `ifn_apc_unique`: 1/4 variable genes (required 2); absent/constant: `CXCL10;GBP1;IRF1`.

No missing module was rescued with a substitute gene set.

## Primary Results: BRL Rim Versus Classical Mixed Rim

| module | difference | Hedges g | exact p | max-T FWER p | bootstrap 95% CI | LOO sign | verdict |
|---|---:|---:|---:|---:|---:|---|---|
| `receptor_cd44_cxcr4` | 1.344 | 2.476 | 0.0002 | 0.0014 | [0.902, 1.823] | stable | `brl_specific_gate_pass` |
| `resolution_efferocytosis_proxy` | 0.419 | 2.071 | 0.0005 | 0.0061 | [0.256, 0.604] | stable | `brl_specific_gate_pass` |
| `lysosomal_unique` | 0.741 | 2.164 | 0.0020 | 0.0073 | [0.418, 1.047] | stable | `brl_specific_gate_pass` |
| `mif_ligand` | 1.160 | 1.678 | 0.0061 | 0.0256 | [0.521, 1.718] | stable | `brl_specific_gate_pass` |
| `mocci_inflammatory_switch` | 1.157 | 1.155 | 0.0416 | 0.2334 | [0.199, 2.017] | stable | `inconclusive` |
| `hla_regulatory` | -0.197 | -0.280 | 0.5790 | 0.9994 | [-0.755, 0.450] | stable | `not_supported` |
| `oxphos` | -0.065 | -0.234 | 0.6497 | 1.0000 | [-0.276, 0.187] | stable | `not_supported` |
| `lipid_repair` | 0.085 | 0.221 | 0.6628 | 1.0000 | [-0.255, 0.449] | unstable | `not_supported` |

The numerically strongest primary module was `receptor_cd44_cxcr4` (difference 1.344, max-T FWER p=0.0014). Its status follows the frozen multi-part gate, not its rank.

## Post-Result Acquisition-Batch Sensitivity

This adversarial sensitivity was specified after the frozen result was visible and therefore cannot confirm or upgrade it. Early slides contained BRL but no mixed-rim AOIs. The source matrix had already been batch-corrected by the authors, but residual acquisition confounding remains plausible. The sensitivity retains only the 4 slides containing both primary lesion types: `DSP-1001660023887-B;DSP-1001660023888-C;DSP-1001660023889-D;DSP-1001660023890-E`.

| module | donors BRL/mixed | difference | exact p | max-T FWER p | LOO sign | sensitivity status |
|---|---:|---:|---:|---:|---|---|
| `lysosomal_unique` | 4/6 | 0.740 | 0.0143 | 0.0524 | stable | does not clear sensitivity |
| `resolution_efferocytosis_proxy` | 4/6 | 0.536 | 0.0143 | 0.0619 | stable | does not clear sensitivity |
| `receptor_cd44_cxcr4` | 4/6 | 1.310 | 0.0190 | 0.1524 | stable | does not clear sensitivity |
| `mocci_inflammatory_switch` | 4/6 | 1.505 | 0.0905 | 0.4286 | stable | does not clear sensitivity |
| `mif_ligand` | 4/6 | 0.676 | 0.2381 | 0.8762 | stable | does not clear sensitivity |
| `lipid_repair` | 4/6 | 0.297 | 0.3476 | 0.9619 | stable | does not clear sensitivity |
| `oxphos` | 4/6 | -0.038 | 0.8952 | 1.0000 | unstable | does not clear sensitivity |
| `hla_regulatory` | 4/6 | 0.075 | 0.9048 | 1.0000 | unstable | does not clear sensitivity |

**No module clears the common-slide max-T sensitivity.** Directions remain positive for several modules, but the available data cannot separate those associations cleanly from acquisition structure.

## Secondary Results: BRL Rim Versus Active Center

Shared donors are removed from both groups before this independent-donor sensitivity analysis.

| module | difference | max-T FWER p | bootstrap 95% CI | verdict |
|---|---:|---:|---:|---|
| `lipid_repair` | -0.542 | 0.0238 | [-0.814, -0.294] | `secondary_contrast_gate_pass` |
| `lysosomal_unique` | -0.645 | 0.0281 | [-0.969, -0.340] | `secondary_contrast_gate_pass` |
| `oxphos` | -0.171 | 0.9416 | [-0.455, 0.161] | `not_supported` |
| `receptor_cd44_cxcr4` | -0.257 | 0.9870 | [-0.833, 0.370] | `not_supported` |
| `hla_regulatory` | -0.147 | 1.0000 | [-0.808, 0.587] | `not_supported` |
| `mocci_inflammatory_switch` | 0.115 | 1.0000 | [-0.980, 1.002] | `not_supported` |
| `resolution_efferocytosis_proxy` | -0.020 | 1.0000 | [-0.219, 0.189] | `not_supported` |
| `mif_ligand` | -0.017 | 1.0000 | [-0.737, 0.621] | `not_supported` |

## Interpretation Boundary

The modules were frozen before this dataset was found, but the source publication already reports broad inflammatory and antigen-presentation enrichment in BRLs. This is therefore a conservative targeted module reanalysis, not independent discovery. Donor aggregation removes AOI pseudoreplication, but the processed deposit lacks NAWM and cannot distinguish every BRL shift from generic lesion activation.

A route may advance only after longitudinal progression association, intervention direction, causal-node specificity, selective perturbation, collateral-function guardrails, CNS exposure, modality fit, and independent replication all hold. None of those requirements is supplied by this analysis alone.

## Provenance

- Primary article: https://doi.org/10.1038/s41591-025-03625-7
- GEO part 1: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE264094
- GEO part 2: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE281805
- Source code: https://github.com/walter-ca/MS-lesions_code
- Input checksums and exact source locations are in `retrieval_manifest.json`.
- Full module coverage, AOI scores, donor-state scores, exact tests, and leave-one-out results are committed beside this report.
