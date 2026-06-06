# V22 Finding: Mixed Locked Validation Of Dynamic APC/HLA-II Response Monitoring

## Executive Verdict

`LOCKED_RULE_V22.md` was committed before validation and then applied without
tuning to reachable held-out cohorts.

The result is mixed and does not reach Tier 4 breakthrough:

- MS dimethyl fumarate (`GSE235357`) passed the locked small-n rule:
  AUC `0.72`, Hedges g `0.65`, `n=10`.
- MS fingolimod (`GSE250453`) failed:
  AUC `0.60`, Hedges g `0.15`, `n=10`.
- Psoriasis adalimumab (`GSE85034_ADA`) failed:
  AUC `0.511`, Hedges g `0.044`, `n=14`.
- UC tofacitinib (`GSE253006_TOF`) passed numerically:
  AUC `1.00`, Hedges g `1.52`, `n=9`, but is exploratory because it uses
  precomputed all-cell module summaries broader than the exact frozen V22
  IFN/APC module and has unresolved compartment mixing.

The rule is not killed either: one reachable MS DMT cohort passed, the locked
kill threshold was not met, and the receptor-control veto did not trigger.

V22 therefore leaves the APC/HLA-II dynamic rule as a provisional
early-treatment monitoring lead, not a validated clinical rule and not a
baseline treatment-selection stratifier.

## What The Rule Predicts

The V22 rule tests early on-treatment change, not baseline state.

Clinical interpretation after V22:

- Supported claim: possible early response-monitoring biology in selected
  therapies, especially MS dimethyl fumarate and UC tofacitinib-like
  immune-remodeling contexts.
- Unsupported claim: prospective baseline patient selection before therapy.
- Unsupported claim: broad cross-disease, cross-therapy transferability.
- Unsupported claim: psoriasis anti-TNF lesional-skin PASI75 monitoring by
  week-1 IFN/APC downshift.

## Mechanistic Interpretation

The surviving signal remains biologically plausible but undervalidated:

- In Class C MS DMTs, the locked feature `delta_HLAII - delta_IFN_APC` is meant
  to capture early APC/HLA-II remodeling relative to inflammatory IFN/APC
  activation.
- The DMF cohort is directionally consistent with this monitoring concept.
- The fingolimod cohort weakens any broad "MS DMT" claim and suggests the
  signal may depend on therapy mechanism, compartment, timing, or small-sample
  instability.
- The psoriasis adalimumab failure argues against assuming the V7 IBD
  mucosal-IFN/APC response-monitoring signal generalizes to unrelated
  tissue/therapy/outcome contexts.
- The UC tofacitinib exploratory pass is consistent with downstream mucosal
  immune remodeling, but cannot be treated as strict locked validation until
  the exact module is recomputed in compartment-resolved data.

## Clinical Utility Status

Current status: not ready for clinical use.

Potential future use if validated:

- decision: early switch versus continue therapy after the first
  transcriptional post-treatment timepoint;
- target population: MS patients starting DMF-like or other immune-remodeling
  DMTs;
- assay: paired baseline and early-treatment blood/PBMC RNA module score;
- action threshold: pre-specified from a larger training cohort, then tested
  prospectively.

The current V22 data are too small and mixed to define a clinical threshold.

## Prospective Falsification Path

Minimum next study:

- enroll `n >= 60` MS patients starting one DMT class, preferably
  dimethyl fumarate or a mechanistically similar immune-remodeling therapy;
- collect blood/PBMC RNA at baseline and a pre-specified early post-treatment
  timepoint between week 1 and week 12;
- compute exactly the frozen V22 modules or a newly locked V23 successor rule
  before outcome analysis;
- primary endpoint: 12-24 month relapse-free/no-evidence-of-disease-activity
  status or a clinically accepted response definition;
- success: AUC `>= 0.70` with lower 95% CI `> 0.55`, effect size Hedges g
  `>= 0.50`, and receptor-control module not outperforming the locked score;
- stop-loss: AUC `< 0.55` or Hedges g `< 0.20` in the correctly timed and
  powered cohort.

## Files

- Locked rule: `LOCKED_RULE_V22.md`.
- Human ledger: `VALIDATION_LEDGER_V22.md`.
- Machine ledger:
  `analysis/v22_locked_apc_hla_validation/validation_ledger_v22.tsv`.
- Cohort search: `COHORT_SEARCH_V22.md`.
- Scripts:
  - `scripts/v22_apply_locked_rule_ms_dmt.py`
  - `scripts/v22_apply_locked_rule_cross_disease.py`

