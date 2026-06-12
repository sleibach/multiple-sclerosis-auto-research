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
| 5 | WS5 internal validation | Deepen synthetic-null/convergence evidence for APC/HLA-II monitoring lead | in-progress | Assemble the full cross-evidence convergence argument for the central lead without making new biological claims. |
| 6 | WS6 infrastructure | Confirm/document SAP RPT true status and consolidate reusable machinery | todo | Do not claim RPT works unless health check verifies it. |
| 7 | WS7 external writeup | Draft skeptical external account of positive/negative results | todo | Publication-grade argument and limitations. |

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
