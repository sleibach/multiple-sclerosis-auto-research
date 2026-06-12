# V44 Queue: Reduce Single-Cohort Dependence

Block start UTC: 2026-06-12T15:20:06Z
Target UTC (+360 min): 2026-06-12T21:20:06Z

## Iterations

| Iteration | Start UTC | End UTC | Status | Notes |
|---|---:|---:|---|---|
| 1 | 2026-06-12T15:20:06Z | 2026-06-12T15:29:44Z | done | Initialized V44. OpenGWAS POST check passed; JWT expires 2026-06-19 12:28 UTC. SAP AI Core Claude/Gemini/RPT smoke-passed. Completed Workstream 1 alternative/replication cohort scout. |

## Backlog

| Priority | Workstream | Item | Status | Notes |
|---:|---|---|---|---|
| 1 | WS1 cohort scout | Exhaustive alternative/replication cohort scout across repositories and literature | done | Wrote `docs/validation/ALT_COHORT_SCOUT_V44.md` and `analysis/v44_alt_cohort_scout/`. No fresh public ready primary Tier 1 cohort found; Gafson remains best Tier 2 target; Karolinska labels are parallel Tier 2; `GSE228330` is open pharmacodynamic/context only. |
| 2 | WS2 batch hardening | Add blind batch-diagnostic guard and rerun synthetic robustness | done | Added additive `batch_diagnostic_metrics.tsv` and `batch_guard_flag` to V42 harness, wrote `docs/validation/BATCH_GUARD_V44.md`, and reran 1,860 synthetic robustness cohorts. Worst response-correlated batch null pass risk fell from `0.40` primary to `0.00` guarded acceptable. |
| 3 | WS3 prereg other leads | Pre-register postpartum APC-arm and T/B compartment monitoring leads | done | Wrote frozen V44 preregistrations and seeded synthetic null/planted mechanics checks. Both synthetic nulls failed and planted signals passed. |
| 4 | WS4 self-audit weak leg | Resolve why V41 joint z is borderline while recurrence is strong | done | Wrote `docs/history/SELF_AUDIT_WEAK_LEG_V44.md`. Joint gate is borderline because the family-wise max-z null is high (`z/null p95=0.988`, FWER `0.0684`); recurrence is more defensible (`78` positive source units vs null p95 `12`, FWER `0.0001`). |
| 5 | WS5 internal validation | Deepen synthetic-null/convergence evidence for APC/HLA-II monitoring lead | done | Wrote `docs/validation/APC_HLA_INTERNAL_CONVERGENCE_V44.md`; ran 20,000-replicate global, modality-aware, and source-local recurrence nulls. APC/HLA/IFN recurrence `78` remains above strictest null p99 `41`; no single modality/source file removal eliminates it. |
| 6 | WS6 infrastructure | Confirm/document SAP RPT true status and consolidate reusable machinery | done | Wrote `meta/INFRASTRUCTURE_STATUS_V44.md` and updated `meta/SAP_AI_CORE_ACCESS_V30.md`. Claude, Gemini, and SAP RPT smoke-pass; Gemini requires non-tiny output-token caps; RPT is genuinely implemented via `/predict`. |
| 7 | WS7 external writeup | Draft skeptical external account of positive/negative results | done | Wrote `docs/reports/EXTERNAL_ACCOUNT_DRAFT_V44.md`, foregrounding no intervention-grade target, provisional monitoring status, confounder/batch bounds, and the Gafson dependence problem. |

## Constraints

- No locked V22 rule changes.
- V42 pre-registration changes, if any, are additive blind tightenings only.
- No reading quarantined or real Gafson validation data.
- Discovery remains closed per V41.
- Synthetic data, if generated, must be seeded, committed, labeled synthetic, and never treated as biological evidence.
- Model/RPT outputs are proposal lenses only; data/source verification decides.
- OpenGWAS POST only; token expiry 2026-06-19 12:28 UTC is flagged.

## Per-Iteration Notes

- Iteration 1 started at 2026-06-12T15:20:06Z.
- Workstream 1 completed at 2026-06-12T15:29:44Z. Search coverage:
  NCBI GEO/PubMed/SRA, Europe PMC, BioStudies/ArrayExpress, Zenodo, Figshare,
  Dryad; ENA/OSF API blockers recorded. Verified ready primary Tier 1 count:
  `0`.
- Next started item: Workstream 2 batch-diagnostic hardening.
- Workstream 2 completed at 2026-06-12T15:36:14Z. V42 harness primary behavior
  remained unchanged on V44 synthetic self-check: null failed, planted signal
  passed. Batch guard reduced worst response-correlated batch synthetic null
  acceptable-pass rate from `0.40` to `0.00`.
- Next started item: Workstream 3 pre-register other live leads.
- Workstream 3 completed at 2026-06-12T15:39:09Z. Wrote
  `docs/validation/POSTPARTUM_APC_ARM_PREREGISTRATION_V44.md`,
  `docs/validation/TB_COMPARTMENT_PREREGISTRATION_V44.md`, and
  `analysis/v44_secondary_lead_harnesses/`. Both synthetic null checks failed
  and both planted checks passed.
- Next started item: Workstream 4 self-audit weak-leg analysis.
- Workstream 4 completed at 2026-06-12T15:42:29Z. The recurrence formulation
  is the stronger internal statement for the APC/HLA-II monitoring lead: `78`
  positive source units vs recurrence-null p95 `12`, empirical FWER `0.0001`.
  The V41 joint z is borderline because the family-wise max-z null is high
  (`8.0548` target z vs null p95 `8.1547`, empirical FWER `0.0684`), not
  because one modality carries the signal.
- Next started item: Workstream 5 internal validation/convergence statement.
- Workstream 5 completed at 2026-06-12T15:47:12Z. Added stricter convergence
  stress tests with 20,000 replicates per null (`global`, `modality`,
  `source_local`). Observed APC/HLA/IFN recurrence `78` exceeded the strictest
  source-local max-null p99 `41` with FWER `0.00005`. Removing
  `treatment_response` leaves recurrence `46`; removing the densest source file
  leaves recurrence `55`, so the convergence is not a single-modality or
  single-report artifact.
- Next started item: Workstream 6 infrastructure/RPT status.
- Workstream 6 completed at 2026-06-12T15:48:44Z. Confirmed SAP AI Core client
  health: Claude 4.7 Opus via Orchestration smoke-passed, Gemini 2.5 Pro
  smoke-passed with `--max-output-tokens 256`, and SAP RPT `sap-rpt-1-large`
  `rpt-smoke` passed through the Python client. Documented reusable validation
  and simulation components.
- Next started item: Workstream 7 skeptical external account.
- Workstream 7 completed at 2026-06-12T15:49:54Z. Drafted a skeptical external
  account in `docs/reports/EXTERNAL_ACCOUNT_DRAFT_V44.md`. The draft states
  the negative target result, the provisional and confounder/batch-bounded
  monitoring status, and why Gafson is necessary but may not be sufficient.
- Seeded V44 backlog complete. Remaining maintenance before final stop:
  update current status / next actions / session log and rebuild the index if
  the repository provides an index command.
