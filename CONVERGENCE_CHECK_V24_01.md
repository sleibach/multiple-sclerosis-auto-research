# CONVERGENCE_CHECK_V24_01

Date: 2026-06-06

## Scout Coverage

V24 searched GEO, BioStudies/ArrayExpress, SRA/ENA, EGA, Zenodo, Figshare,
OSF, PubMed/Europe PMC, preprint queries, consortium/portal routes, and
partially used local cohorts for fresh treatment-response transcriptomic
validation data.

## Direct Verdict

The public ready-to-run well is effectively dry for a primary APC/HLA-II
monitoring validation cohort: no clean public n>=30 fresh MS DMT cohort with
paired baseline/early-treatment transcriptomics and responder labels was
verified.

The low-barrier well is not dry. The best next source is Gafson et al. 2018
DMF PBMC RNA-seq (PMID `30283812`, DOI
`10.1212/nxi.0000000000000470`), which matches the target scientifically but
requires author/data access for processed counts and sample-level NEDA-4 labels.

## Usable or Near-Usable Sources

- `GSE130478/GSE130491/GSE130494`: public DMF longitudinal data, but response
  labels are absent from GEO metadata and expression timing is 6 months, not the
  V22 early window.
- `GSE85034_MTX`: local/open unused psoriasis methotrexate arm, 13 PASI75-
  labeled subjects, paired baseline/week16 lesional skin. Secondary stress test
  only.
- `GSE253495`: RA upadacitinib CD14 monocyte RNA-seq, paired baseline/3 months
  but all patients improved, so no response-discrimination validation.

## Next Action

Acquire the Gafson et al. 2018 data and labels first. If unavailable, acquire
response-label mapping for `GSE130478/GSE130491/GSE130494`. Do not create or
test a V23 successor rule until fresh held-out data are actually available.
