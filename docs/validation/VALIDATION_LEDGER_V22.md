# V22 Locked APC/HLA-II Validation Ledger

Locked rule: `LOCKED_RULE_V22.md`, committed before held-out validation in
commit `013639b`.

Machine-readable ledger:
`analysis/v22_locked_apc_hla_validation/validation_ledger_v22.tsv`.

## Primary Locked Cohorts

| Cohort | Disease | Therapy | Class | n | Feature | AUC | 95% CI | Hedges g | Result | Interpretation |
|---|---:|---|---|---:|---|---:|---|---:|---|---|
| GSE235357 | MS | dimethyl fumarate | Class C | 10 | `delta_HLAII - delta_IFN_APC` | 0.720 | 0.310-1.000 | 0.651 | pass | Small-n suggestive early-monitoring signal; wide CI prevents strong claim. |
| GSE250453 | MS | fingolimod | Class C | 10 | `delta_HLAII - delta_IFN_APC` | 0.600 | 0.167-1.000 | 0.150 | fail | Does not meet locked threshold. |
| GSE85034_ADA | psoriasis | adalimumab | Class A | 14 | `-delta_IFN_APC` | 0.511 | 0.077-0.911 | 0.044 | fail | No locked-rule signal in lesional-skin week-1 PASI75 prediction. |

## Exploratory / Not Counted As Primary Validation

| Cohort | Disease | Therapy | Class | n | Feature | AUC | 95% CI | Hedges g | Result | Why Exploratory |
|---|---:|---|---|---:|---|---:|---|---:|---|---|
| GSE253006_TOF | ulcerative colitis | tofacitinib | Class A | 9 | `-delta_IFN_APC` approximation | 1.000 | 1.000-1.000 | 1.522 | pass | Uses precomputed all-cell sample summaries with a broader IFN/APC module (`STAT1;IRF1;CXCL10;GBP1;CD74;IFI30;HLA-DRA;HLA-DRB1`) rather than the exact frozen seven-gene module. Compartment unresolved. |

## Receptor-Control Check

The receptor-control module did not outperform the locked score by `>= 0.10`
in two cohorts. Receptor AUCs were:

- GSE235357: `0.36`, below the locked score by `0.36`.
- GSE250453: `0.40`, below the locked score by `0.20`.
- GSE85034_ADA: `0.556`, above the locked score by `0.044`, below the
  non-specificity threshold.
- GSE253006_TOF: `0.80`, below the locked score by `0.20`.

## Locked-Threshold Verdict

V22 does not satisfy the breakthrough threshold:

- Required: at least three held-out cohort passes, including at least one MS
  DMT pass and at least two therapy classes.
- Observed primary locked validation: one small-n MS DMT pass, two primary
  failures.
- Observed exploratory support: one UC tofacitinib pass, not countable as
  primary locked validation because the module was approximate.

V22 also does not meet the locked kill threshold:

- Not every reachable MS DMT cohort failed, because GSE235357 passed the
  small-n rule.
- There were not at least three primary locked failures.
- The receptor-control veto did not trigger.

Therefore the rule remains a provisional early-treatment monitoring lead, not a
validated clinical rule and not a killed hypothesis.

