# V17 GPR25 Mechanism Artifacts

Date: 2026-06-06

Primary report: `../../GENETICS_GPR25_WORKUP_V17.md`

## Key Outputs

- `eqtlgen_full_extract/chr1_candidate_gene_full_rows.tsv`:
  streamed extract from the full eQTLGen cis file for chr1 candidate genes
  (`GPR25`, `DDX59`, `KIF21B`, `C1orf106`).
- `eqtlgen_full_chr1_candidate_gene_summary.tsv`:
  candidate-gene eQTLGen summary across all extracted rows.
- `eqtlgen_full_chr1_candidate_shared_variant_summary.tsv`:
  eQTLGen summary restricted to the MS-UC shared credible-set variants.
- `eqtl_coloc_chr1/`:
  bounded disease-vs-eQTL SuSiE-coloc runs for `GPR25`, `KIF21B`, `DDX59`,
  and `C1orf106`.
- `gse301908_gene_expression_by_majorcluster.tsv`:
  local MS CNS single-nucleus major-cluster expression check.
- `h5ad_gene_presence_expression.tsv` and
  `h5ad_gene_expression_by_celltype.tsv`:
  local h5ad cross-atlas expression scans for `GPR25`, `KIF21B`, and `CXCL17`.
- `raw_api/`:
  cached UniProt, ChEMBL, AlphaFold, ClinicalTrials.gov, Europe PMC, PubMed,
  GEO, and Google Patents responses used for mechanism, druggability, novelty,
  and data-availability checks.

## Reproducible Entry Points

- `../../scripts/v17_extract_eqtlgen_chr1_candidates.sh` regenerates the
  streamed full-eQTLGen chr1 candidate-gene extract. It uses `curl -k` because
  the eQTLGen download host currently presents an expired TLS certificate.
- `../../scripts/v17_scan_h5ad_gpr25_kif21b.py` regenerates the h5ad expression
  tables.
- `../../scripts/v17_summarize_gpr25_checkpoint.py` prints the key numeric
  checkpoint values from the saved TSV outputs.
- `eqtl_coloc_chr1/run_eqtl_susie_coloc.R` and
  `eqtl_coloc_chr1/run_competitor_eqtl_susie_coloc.R` regenerate the bounded
  eQTL SuSiE-coloc summaries.

## Interpretation Guardrail

The chr1 locus is unresolved between `GPR25` and `KIF21B`.

- `GPR25` has stronger eQTL signal in the disease-shared block and a plausible
  CXCL17-GPR25 GPCR ligand axis, but weak transcript-level cell-state support.
- `KIF21B` has stronger single-cell expression support but poor direct
  druggability and prior art as an MS/IBD susceptibility locus.

Do not treat either gene as exclusively causal or intervention-grade without
protein-level, genotype-linked, or stronger tissue-specific QTL evidence.
