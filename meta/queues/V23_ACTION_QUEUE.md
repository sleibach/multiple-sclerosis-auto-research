# V23 Action Queue - APC/HLA-II Monitoring Lead

Initialized: 2026-06-06 14:18 CEST

Rule discipline: `docs/locked_rules/LOCKED_RULE_V22.md` is immutable. V23 may pool,
characterize, or bound the existing rule. Any improved rule must be a separate
successor lock and cannot be tested on data that motivated it.

## Queue

| Action | Status | Notes |
|---|---|---|
| 1. Pool the small cohorts | completed | Primary locked pooled AUC `0.547`, stratified bootstrap CI `0.337-0.743`; primary fixed/random-effects Hedges g `0.254`, CI `-0.437-0.945`. Including exploratory UC gives AUC `0.594`, CI `0.411-0.764`. |
| 2. Characterize drug-mechanism specificity | completed | Exact UC cleanup makes the bounded domain stronger: primary plausibly-in-scope cohorts DMF and exact UC tofacitinib both pass; fingolimod/S1P and psoriasis lesional adalimumab fail. |
| 3. Resolve disqualified tofacitinib | completed | Exact frozen V22 all-cell raw 10x rescoring passes: AUC `0.95`, CI `0.70-1.00`, Hedges g `1.811`, n `9`; compartment remains unresolved. |
| 4. Mechanistic grounding | completed | Exact UC signal is strongest in marker-derived `t_cell_like` (AUC `1.00`, g `1.27`, receptor AUC `0.60`) and `b_plasma_like` (AUC `0.95`, g `1.49`, receptor AUC `0.75`); myeloid is positive but weaker (AUC `0.80`). Signal is not APC-only and likely tracks broader cytokine/JAK-STAT immune remodeling. |
| 5. Clinical utility statement | completed | Monitoring use only: baseline plus earliest post-treatment sample, most plausible for immune-remodeling/JAK-STAT contexts; decision is continue vs early switch/escalate, not pretreatment selection. |
| 6. Successor rule decision | completed | Do not lock V23 successor rule in this session: bounded domain is plausible, but only two small primary in-scope cohorts and no fresh held-out dataset remain for an honest successor test. |

## Live Loop Notes

- 2026-06-06 14:18 CEST: OpenGWAS access verified. V22 state read. Local
  cohorts confirmed: GSE235357, GSE250453, GSE85034, GSE253006.
- 2026-06-06 14:20 CEST: Action 1 completed. Immediate next action plausible:
  mechanism-specificity analysis, because the pooled primary locked signal is
  weak while DMF and exploratory tofacitinib remain directionally stronger.
- 2026-06-06 14:24 CEST: Actions 2-3 completed. Exact GSE253006 rescoring
  resolves the module-approximation disqualification at all-cell level and
  supports a bounded immune-remodeling/JAK-STAT domain. Immediate next action:
  mechanistic grounding and clinical utility, since a successor rule may be
  warranted but needs a clear domain statement first.
- 2026-06-06 14:30 CEST: Action 4 completed with exact marker-derived
  compartment rescoring. The UC signal is not restricted to myeloid/APC;
  T-cell-like and B/plasma-like compartments are strongest. Actions 5-6
  completed in synthesis: clinical use remains monitoring-only; no V23
  successor rule is locked because no unused held-out dataset remains.
