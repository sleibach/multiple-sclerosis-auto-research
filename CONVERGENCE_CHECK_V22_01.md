# CONVERGENCE_CHECK_V22_01

Timestamp: 2026-06-06 14:10 CEST

## Validation State

Primary locked cohorts tested:

- `GSE235357` MS dimethyl fumarate: pass, but small-n and wide CI.
- `GSE250453` MS fingolimod: fail.
- `GSE85034_ADA` psoriasis adalimumab: fail.

Exploratory cohort:

- `GSE253006_TOF` UC tofacitinib: numerical pass, but not counted as primary
  locked validation because the module is a precomputed approximation and
  compartment is unresolved.

## Agreement / Disagreement

Agreement with prior project state:

- The signal remains most compatible with an early monitoring readout, not a
  baseline stratifier.
- IBD-like mucosal immune remodeling remains more plausible than broad
  cross-disease treatment-response transfer.

Disagreement / weakening:

- The locked dynamic rule does not generalize cleanly to all MS DMTs:
  fingolimod failed while dimethyl fumarate passed.
- The rule does not generalize to psoriasis adalimumab lesional skin.

## Current Verdict

No Tier 4 breakthrough. No kill. The dynamic APC/HLA-II rule remains a
provisional monitoring lead requiring larger independent MS DMT validation.

## Next Forcing Question

Can the small-n DMF pass replicate in a larger MS DMT cohort with paired
baseline and early-treatment transcriptomics, or is it sampling instability?

