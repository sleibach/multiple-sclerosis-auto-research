# Decision 0017: NAMPT eNAMPT-vs-iNAMPT Tier 0 Audit

Date: 2026-05-28

## Decision

`NAMPT` is demoted from alive Tier 0 to a marker/readout branch.

## Rationale

The constrained V4 branch was not generic systemic NAMPT inhibition; it asked
whether extracellular NAMPT or a biomarker-defined transient NAMPT-axis state
could be separated from intracellular NAMPT/NAD stress-metabolism biology.

The local Tier 0 audit did not support that separation:

- MS white-matter delta log2 `-0.2143688948990014`, p `0.5434156214094958`.
- Non-IBD retained positive disease count `0`.
- Strict core-covariate surviving disease count `0`.
- OpenTargets max genetics score `0.0`.
- Positive C15-like contexts were Crohn myeloid, UC myeloid, and T1D acinar
  cell, not MS.
- No local evidence demonstrated a non-NAD-depleting eNAMPT-specific or
  tissue-bounded modality.

This is not a P0 prior-art invalidation. It is an evidence-driven Tier 0
failure for active therapeutic nomination. Retain NAMPT only as a marker/readout
for HIF/NAD/eNAMPT inflammatory metabolism.

## Trace

- Script: `scripts/tier0_nampt_enampt_audit.py`
- Outputs:
  - `analysis/tier_0_triage/nampt_enampt_separation/REPORT.md`
  - `analysis/tier_0_triage/nampt_enampt_separation/decision.json`
  - `analysis/tier_0_triage/nampt_enampt_separation/evidence_matrix.tsv`
