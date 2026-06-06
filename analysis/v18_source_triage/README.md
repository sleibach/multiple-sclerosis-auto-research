# V18 Source Triage Artifacts

Date: 2026-06-06

Primary plan: `../../meta/DATA_ACQUISITION_PLAN_V18.md`

## Verification Tables

- `candidate_urls.tsv`: candidate source URLs evaluated in V18.
- `url_verification.tsv`: HTTP/HEAD verification results for source URLs.
- `dice_significant_url_verification.tsv`: DICE significant eQTL VCF endpoint
  verification.
- `eqtl_catalogue_studies_curl_verbose.txt`: eQTL Catalogue REST API HTTP 500
  evidence.

## Acquired-Source Outputs

- `acquired_sha256.tsv`: SHA-256 checksums for all acquired Tier 1 files under
  `data/raw/v18_source_triage/`.
- `acquired_smoke_tests.tsv`: first-pass schema/queryability smoke tests.
- `target_gene_eqtl_hits.tsv`: target-gene eQTL hits from acquired OneK1K and
  DICE data.
- `v18_hits_vs_v17_credible_set.tsv`: fast position-overlap check between
  acquired OneK1K/DICE KIF21B hits and the V17 shared MS-UC credible set.
- `dice_mean_expression_target_genes.tsv`: DICE mean TPM for `GPR25`, `KIF21B`,
  and `CXCL17`.

## Reproducible Entry Point

- `../../scripts/v18_smoke_test_acquired_sources.py` regenerates
  `target_gene_eqtl_hits.tsv` and `dice_mean_expression_target_genes.tsv` from
  acquired files.

## Key V18 Result

The self-acquired public genotype-linked immune eQTL data currently favors
`KIF21B` over `GPR25` as the transcript-visible chr1 candidate:

- OneK1K top-eQTL summaries: `14` target hits, all `KIF21B`.
- DICE significant eQTL panel: `1` target hit, `KIF21B` in NK cells.
- DICE mean expression: `KIF21B` is high across immune subsets, while `GPR25`
  is low but nonzero in selected T/NK subsets.
- eQTL Catalogue targeted QTD000021 extract: `8,416` target rows, all `KIF21B`.
- The OneK1K/DICE top/significant KIF21B hits do not exactly match the V17
  shared credible-set variants; nearest observed distances were `17,230 bp` and
  `21,012 bp` for two OneK1K hits.

This does not fully resolve causality because public top/significant summaries
can miss weaker or cell-state-specific GPR25 effects, and no protein/CITE-seq
MS source was acquired.
