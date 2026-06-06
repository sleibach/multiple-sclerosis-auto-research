# ORCHESTRATION_LOG_V16

Date: 2026-06-06

## Session Start

- OpenGWAS token verified with `scripts/check_opengwas_access.py`; `/user` HTTP 200; token valid until `2026-06-19 12:28 UTC`.
- Read `meta/MATRIX_STATUS.md`, `meta/NEXT_ACTIONS.md`, and `GENETICS_LOCI_WORKUP_V15.md`.

## eQTL Pre-flight

- GTEx Portal API reachable:
  - `https://gtexportal.org/api/v2/dataset/tissueSiteDetail` returned HTTP 200 by GET.
  - OpenAPI spec reachable at `https://gtexportal.org/api/v2/openapi.json`.
  - Relevant endpoints found: `/api/v2/reference/gene`, `/api/v2/dataset/variant`, `/api/v2/association/singleTissueEqtl`, `/api/v2/association/singleTissueEqtlByLocation`.
- Stale GTEx Google Storage full-archive URLs tested:
  - `https://storage.googleapis.com/gtex_analysis_v8/single_tissue_qtl_data/GTEx_Analysis_v8_eQTL.tar` returned HTTP 404.
  - `https://storage.googleapis.com/gtex_analysis_v8/single_tissue_qtl_data/GTEx_Analysis_v8_eQTL_EUR.tar` returned HTTP 404.
  - No `x-deny-reason`; host was reachable but these paths are stale/not canonical.
- eQTLGen:
  - `https://www.eqtlgen.org/` returned HTTP 200.
  - `https://www.eqtlgen.org/cis-eqtls.html` returned HTTP 200.
  - Full data access not yet resolved in this session.
- eQTL Catalogue:
  - `https://www.ebi.ac.uk/eqtl/api/` HEAD returned HTTP 405 (method not allowed).
  - `https://www.ebi.ac.uk/eqtl/api/datasets` returned HTTP 404.
  - No `x-deny-reason`; endpoint path likely stale rather than proxy blocked.

Downgrade decision: use GTEx API as the first reachable allele-level QTL source.
This is not full raw GTEx/eQTLGen summary-statistic colocalization. A GTEx API
result can confirm significant eQTL direction for exact variant/gene/tissue
pairs, but absence from the significant endpoint is not a formal absence of
eQTL effect.

Supplemental eQTLGen access:

- The eQTLGen significant cis-eQTL file was downloaded with `curl -k` because
  `download.gcc.rug.nl` has an expired TLS certificate under normal Python
  verification.
- File:
  `data/raw/eqtlgen_cis_eqtl/2019-12-11-cis-eQTLsFDR0.05-ProbeLevel-CohortInfoRemoved-BonferroniAdded.txt.gz`
- SHA-256:
  `8d963046d7b74cf3533c3510614cdc724e7ad0e325a3d2f7cca63ad13661b4c4`
- README SHA-256:
  `9f61a616f6276de6d45a7e35577b50596b95d3e76e2ad3c3932cb18f10cd6bdc`
- Exact candidate rows were extracted to
  `analysis/v16_eqtl_workup/eqtlgen_exact_candidate_alignment.tsv`.

## Subagent Dispatch

Attempted to spawn three worker subagents:

- GPR25 chr1 MS-UC
- ZMIZ1 chr10 MS-Crohn
- PTGER4 chr5 signal decomposition

All three spawn attempts failed with: `agent thread limit reached`.

Operational downgrade: run the three workstreams sequentially as labeled
subagent-equivalent reports, with disjoint outputs under `subagents/`.
