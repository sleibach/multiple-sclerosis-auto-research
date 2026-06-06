# CONVERGENCE_CHECK_V13_01

Timestamp: 2026-06-05 16:11 CEST

## Access State

OpenGWAS access works when `.env` is loaded explicitly.

Verification command:

- `.venv/bin/python scripts/check_opengwas_access.py`

Verified endpoints:

- `/user`: HTTP `200`.
- POST `/gwasinfo` for `ieu-b-18`: HTTP `200`.
- POST `/tophits` for `ieu-b-18`: HTTP `200`.

## Work Completed

Created and ran:

- `scripts/v13_opengwas_coloc_uc_crohn.py`
- `scripts/v13_annotate_coloc_regions.py`

Outputs:

- `analysis/v13_genetics_coloc/opengwas_tophits.tsv`
- `analysis/v13_genetics_coloc/shared_tophit_regions.tsv`
- `analysis/v13_genetics_coloc/coloc_region_summary.tsv`
- `analysis/v13_genetics_coloc/coloc_region_summary_annotated.tsv`
- `analysis/v13_genetics_coloc/coloc_snp_abf.tsv`
- `analysis/v13_genetics_coloc/REPORT.md`

## Results

Regions analyzed:

- `34` shared top-hit windows.

High-H4 first-pass regions:

- MS-UC:
  - `1:200375242-201375897`, `PP.H4 = 0.9840`.
  - `5:39896425-40944986`, `PP.H4 = 0.9337`.
- MS-Crohn:
  - `10:80542475-81559335`, `PP.H4 = 0.9776`.
  - `17:40014201-41029835`, `PP.H4 = 0.9413`.

High-H3 distinct-causal pattern:

- Multiple MHC windows in both UC and Crohn favored `PP.H3 ~= 1` rather than
  shared causality.

## Matrix Grade Decision

No matrix grade was upgraded in this checkpoint.

Reason:

- The coloc layer is real and executable, but it is single-causal-variant and
  selected from overlapping top hits.
- Full robust-grade genetics still requires genome-wide rg rerun, MHC-excluded
  sensitivity, multi-signal coloc, and eQTL/pQTL causal-gene mapping.

## Current Interpretation

The V12 gut genetics finding is partially hardened but also sharpened:

- UC and Crohn both show non-HLA MS shared-locus signals in first-pass coloc.
- HLA overlap is not a simple shared-causal-variant story in this analysis.
- The claim that UC is genetically closer than Crohn still rests on published
  genome-wide `rg`; V13 has not yet rerun LDSC/HDL.

## Next Session First Action

Continue V13 genetics robustification:

1. Run or scaffold genome-wide LDSC/HDL for MS-UC and MS-Crohn using
   OpenGWAS-accessible summary statistics.
2. Run multi-signal SuSiE-coloc on the four high-H4 regions and the H3 MHC
   negative-control regions.
3. Add eQTL/pQTL coloc for the high-H4 regions before assigning causal genes.
