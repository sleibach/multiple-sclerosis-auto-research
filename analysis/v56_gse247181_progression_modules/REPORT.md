# V56 Rapid-Versus-Slow SPMS PBMC Module Test

## Verdict

**No pre-existing V54 progression route cleared the frozen rapid-versus-slow SPMS association gate.**

This is a frozen, cross-sectional reanalysis of 10 deposited rapid/aggressive and 10 slow untreated SPMS participants. It is not prospective prediction, causality, treatment response, evidence that an intervention slows disability, or a therapeutic target.

## Cohort And Processing

- Exactly 20 pre-eligible CEL files were processed together: 10 `SPMS-a` (rapid/aggressive) and 10 `SPMS-s` (slow), all deposited as untreated.
- Core-transcript RMA was run with `oligo` 1.76.0 and `pd.clariom.d.human` 3.14.1; identifiers used `clariomdhumantranscriptcluster.db` 8.8.0.
- Frozen-module coverage: 9/9 valid. No module was outcome-adapted.
- Every primary test enumerated all 184,756 possible 10/10 label assignments; max-T controlled the complete valid-module family.
- Synthetic calibration: 285/6000 null families passed (rate 0.0475; one-sided p for excess over 0.05=0.8204); independent naive and vectorized exact engines matched=True; planted signals passed in all three seeds. Synthetic results characterize code only.

## Frozen Primary Results

| module | rapid-slow difference | Hedges g | exact p | max-T FWER p | bootstrap 95% CI | LOO sign | verdict |
|---|---:|---:|---:|---:|---:|---|---|
| `receptor_cd44_cxcr4` | -0.603 | -0.730 | 0.1057 | 0.6101 | [-1.276, 0.053] | stable | `not_supported` |
| `lysosomal_unique` | -0.567 | -0.804 | 0.0772 | 0.6725 | [-1.113, 0.006] | stable | `not_supported` |
| `hla_regulatory` | 0.243 | 0.234 | 0.5940 | 0.9955 | [-0.599, 1.054] | stable | `not_supported` |
| `ifn_apc_unique` | 0.240 | 0.301 | 0.4943 | 0.9960 | [-0.367, 0.885] | stable | `not_supported` |
| `lipid_repair` | -0.213 | -0.320 | 0.4955 | 0.9984 | [-0.763, 0.276] | stable | `not_supported` |
| `mif_ligand` | 0.137 | 0.125 | 0.7708 | 1.0000 | [-0.736, 0.969] | unstable | `not_supported` |
| `oxphos` | -0.103 | -0.151 | 0.7250 | 1.0000 | [-0.664, 0.418] | unstable | `not_supported` |
| `mocci_inflammatory_switch` | 0.032 | 0.022 | 0.9608 | 1.0000 | [-1.101, 1.198] | unstable | `not_supported` |
| `resolution_efferocytosis_proxy` | -0.002 | -0.005 | 0.9915 | 1.0000 | [-0.304, 0.292] | unstable | `not_supported` |

## Technical And Demographic Audit

- Sex counts were rapid {'F': 9, 'M': 1} and slow {'F': 8, 'M': 2} (Fisher exact p=1.0000). Age was not deposited, so the frozen secondary age/sex model could not run.
- The R-number embedded in deposited CEL names differs by group. GEO does not identify it as assay order or batch, so it is a design warning rather than a confirmed technical confounder.
- RMA distribution and global-PCA diagnostics were tested as a separate max-T family and did not remove samples. Results:

| diagnostic | standardized rapid-slow difference | exact p | max-T FWER p |
|---|---:|---:|---:|
| `raw_median_intensity` | -0.588 | 0.2130 | 0.6375 |
| `raw_intensity_iqr` | -0.577 | 0.2186 | 0.6512 |
| `normalized_median` | 0.521 | 0.2637 | 0.7278 |
| `pca1` | -0.437 | 0.3530 | 0.8416 |
| `deposited_file_r_number` | 0.350 | 0.5117 | 0.9356 |
| `pca2` | 0.343 | 0.4707 | 0.9397 |
| `normalized_iqr` | -0.178 | 0.7201 | 0.9959 |

## Therapeutic Boundary

A module that clears this association gate would still need pathogenic direction, causal-node specificity, selective functional perturbation, collateral guardrails, CNS exposure, modality fit, and independent longitudinal replication. A failed or inconclusive module is not rescued by its effect-size rank. No result here is intervention-grade.

## Reproducibility

- Frozen plan: `docs/plans/V56_GSE247181_RAPID_SLOW_PROGRESSION_TEST.md`
- Selector/downloader: `scripts/v56_prepare_gse247181.py`
- RMA processor: `scripts/v56_process_gse247181.R`
- Exact analysis: `scripts/v56_analyze_gse247181.py`
- Public source: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247181
- Every input URL, expected byte count, and local SHA-256 is in `retrieval_manifest.tsv`; raw CEL files remain ignored.
