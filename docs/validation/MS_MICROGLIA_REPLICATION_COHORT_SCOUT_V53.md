# MS Microglia Replication Cohort Scout V53

Status: public-data eligibility audit and frozen-score execution record. It
does not change V22, V42, or any locked validation rule.

## Candidate Audit

| source | verified structure | target-gene coverage | decision |
|---|---|---|---|
| [Macnair et al. Zenodo 8338963 discovery cohort](https://zenodo.org/records/8338963) | 54 MS and 26 control donors; 155 eligible samples; 51,677 deposited microglia; age, sex, lesion class, PMI, and sequencing pool | all 16 frozen genes | **Run.** Frozen primary passes; conservative microglia-depth tightening is borderline. |
| [Macnair et al. Zenodo 8338963 validation matrix](https://zenodo.org/records/8338963) | after deterministic cross-study donor de-duplication: 18 MS and 13 controls; 47 samples; 11,222 microglia; age, sex, study, lesion class, and PMI | all 16 frozen genes | **Run.** Frozen and depth-tightened primary pass. |
| [GSE301908](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE301908) | 14 MS and 3 controls; white-matter snRNA-seq; deposited major-cell annotation; age/sex available through the paired study metadata | all 16 frozen genes in the held RDS | Eligible only for a very low-control third sensitivity; not counted as replication in this audit. |
| `GSE180759` | 5 MS and 3 controls; lesion/periplaque/control white matter; deposited immune annotation | score genes available in the parent matrix | Already represented as `a2021` inside the Macnair validation composite; cannot be counted again independently. |
| `GSE284005` | 14 MS and 3 controls; 500-gene MERFISH companion to GSE301908 | panel-limited and paired to GSE301908 | Not an independent donor cohort and not used for the frozen transcriptome score. |
| `GSE279972` | 28 MS and 10 control donors; lesion-region tissue multi-omics/proteomics | not a donor-level purified-microglia transcriptome | Ineligible for the frozen replication definition. |

No cohort was counted merely for containing MS or microglia. The two executed
matrices have donor labels, disease labels, frozen annotation, all target genes,
and the required covariates. Raw multi-gigabyte matrices remain at Zenodo and
were streamed, never committed.

## Reproduction

1. Generate deposited-order microglial column maps with
   `scripts/v53_prepare_macnair_microglia_metadata.py`.
2. Compile `scripts/v53_targeted_matrix_market_pseudobulk.cpp` with a C++17
   compiler.
3. Stream the corresponding Zenodo Matrix Market gzip through the extractor;
   use the checksums in each `metadata_preparation_summary.json`.
4. Run `scripts/v53_analyze_macnair_microglia_replication.py` with cohort
   `validation` or `discovery`.

Outputs and exact results are under
`analysis/v53_ms_microglia_independent_cohort_scout/`.
