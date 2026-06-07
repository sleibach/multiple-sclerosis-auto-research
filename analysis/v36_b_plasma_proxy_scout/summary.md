# V36 Cross-Disease B/Plasma Proxy Scout

Status: **blocked for independent replication with held data**.

## Question

After V36 refined the top T/B lead toward a B/plasma-like IFN/APC dynamic
carrier, this scout asked whether any held paired treatment-response cohort
outside `GSE253006` can test that carrier with B/plasma proxies.

## Held Artifacts Searched

- `analysis/v22_locked_apc_hla_validation/`
- `analysis/v23_apc_hla_monitoring/`
- `analysis/tier_0_triage/hyp_v6_006_gse138064_ms_ifnb_replication/`
- `analysis/tier_0_triage/hyp_v6_006_gse24427_ms_ifnb_longitudinal/`
- `analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/`

Marker scan included:

- B/plasma markers: `MS4A1`, `CD79A`, `CD79B`, `MZB1`, `JCHAIN`, `XBP1`,
  `CD38`, `SDC1`.
- Locked-module genes: `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`,
  `HLA-DRA`, HLA-II genes, `CD44`, `CXCR4`.

## Result

- `GSE253006_TOF_exact` remains the only held response cohort with saved
  compartment-resolved paired scores.
- MS IFN-beta response artifacts (`GSE138064`, `GSE24427`) contain locked
  module scores and gene coverage, but not a saved B/plasma marker or
  compartment-deconvolution score sufficient to test the refined B/plasma
  carrier.
- V22/V23 paired ledgers contain IFN/APC, HLA-II, receptor, and locked scores,
  but not B/plasma-specific features outside `GSE253006`.
- The marker scan found `CD38` in a pregnancy decoupling module, but that is not
  a paired treatment-response B/plasma carrier test.

## Verdict

**Independent B/plasma replication is blocked with held data.** The refined
carrier is better specified than V35, but still depends on one compartment-
resolved UC tofacitinib cohort.

## Required Next Test

Independent paired treatment-response data with either:

- single-cell/sorted B/plasma/T/myeloid expression; or
- bulk expression plus a pre-specified validated B/plasma deconvolution model;

and patient-level response labels, steroid/infection metadata, and early
on-treatment timepoints. The frozen test should score B/plasma IFN/APC delta,
T-cell IFN/APC delta, non-T/B IFN/APC delta, and abundance-adjusted residuals
before any outcome inspection.
