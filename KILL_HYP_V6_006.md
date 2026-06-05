# KILL_HYP_V6_006 - Locked Cross-Disease APC Response Rule

Date: 2026-05-28  
Rule killed: `LOCKED_RULE_V7.md`  
Commit preceding validation: `27605b3`

## Verdict

The locked V7 cross-disease APC response architecture rule is killed as a
general autoimmune treatment-response stratifier. It met the pre-specified kill
threshold: at least three independent in-scope validation cohorts failed, with
at least two showing AUC `<0.55` or Hedges g `<0.20`.

This is not a kill of every APC-plasticity hypothesis. The failure mode is
specific and informative: the **baseline Class A fallback fails reproducibly**,
while **mucosal IBD early IFN/APC downshift validates in two independent paired
infliximab cohorts**.

## Validation Ledger Summary

Source: `analysis/v7_validation/v7_validation_summary.tsv`.

| Cohort | Disease | Feature | N | AUC | Hedges g | Result |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `GSE16879` | IBD | `-delta_IFN_APC` | 60 | 0.754 | 0.985 | pass |
| `GSE73661_IFX` | UC | `-delta_IFN_APC` | 23 | 0.825 | 1.390 | pass |
| `GSE8350` | RA | `-delta_IFN_APC` | 18 | 0.450 | -0.356 | fail |
| `GSE12051` | RA | `baseline_IFN_APC` | 44 | 0.382 | -0.339 | fail |
| `GSE12251` | UC | `baseline_IFN_APC` | 22 | 0.250 | -1.043 | fail |
| `GSE138746_CD14` | RA | `baseline_IFN_APC` | 78 | 0.485 | -0.099 | fail |

## Interpretation

The locked rule bundled two claims:

1. Dynamic Class A response is captured by early IFN/APC downshift.
2. If early samples are absent, high baseline IFN/APC is an adequate fallback.

The validation data reject claim 2. They do not reject claim 1 in mucosal IBD;
instead, claim 1 is strengthened there and weakened in RA whole blood.

## Failure Modes Converted To Tier -1 Hypotheses

1. `HYP_V7_001`: In mucosal IBD, early tissue IFN/APC downshift after
   infliximab is the response-linked variable; baseline IFN/APC is not a valid
   substitute.
2. `HYP_V7_002`: APC plasticity is compartment-restricted; inflamed intestinal
   mucosa shows a measurable responder downshift, while RA peripheral blood does
   not.
3. `HYP_V7_003`: RA anti-TNF response may require synovial-tissue APC
   plasticity rather than blood IFN/APC architecture; blood failures are
   compartment mismatch, not necessarily target-mechanism absence.
4. `HYP_V7_004`: Receptor-only CD74/CD44/CXCR4 is not the dominant predictor;
   where it is scoreable, it tracks the dynamic IFN/APC result but does not
   outperform it by the locked specificity veto.

## Next Required Step

Promote `HYP_V7_001` to Tier 0 immediately. It has two independent paired
validation passes in IBD and a clear therapeutic use case: early pharmacodynamic
stratification after first anti-TNF exposure. It is not yet Tier 4 because it is
not cross-therapy, not causal, and currently disease/compartment-limited.
