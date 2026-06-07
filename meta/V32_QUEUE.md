# V32 Queue: Treatment-Response Confounder Audit

Last updated: 2026-06-07 10:20 UTC

## Completed This Session

- Verified OpenGWAS token and SAP AI Core model access.
- Queried the local knowledge index before analysis.
- Built and ran `scripts/v32_confounder_audit.py`.
- Scored frozen raw-expression confounder panels on the bounded V22/V23 cohorts:
  `GSE235357` and exact raw-10x `GSE253006_TOF`.
- Wrote the audit report:
  `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md`.
- Updated validation readiness:
  `docs/validation/VALIDATION_READINESS_V27.md`.

## Result

- Single-panel tests: all `23 / 23` confounder scores classified as `survives`.
- Baseline APC/HLA-II + glucocorticoid joint adjustment: survives.
- Cell-composition joint adjustment: survives.
- Broad metabolic/inflammatory/STAT1 joint adjustment: attenuates but does not
  explain away the signal.
- Overall V32 verdict: partially confounded / immune-tone bounded, not a
  glucocorticoid or cell-composition artifact.

## Next Actions

1. When the fresh Gafson/NEDA or equivalent cohort arrives, quarantine it and
   run the frozen V22 validation harness plus the V32 confounder panels without
   tuning.
2. If no fresh validation cohort is available, advance the postpartum
   HLA-II/CD64 APC-axis biology lead from V29/V31 using existing data.
3. Optional hardening: add a direct steroid-pulse public-data scout so the
   glucocorticoid signature panel can be benchmarked against known steroid
   exposure rather than only inferred from expression.
