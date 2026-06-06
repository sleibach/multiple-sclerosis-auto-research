# CONVERGENCE_CHECK_6 - SQLE Fail-Fast Closure and Pivot

Timestamp: 2026-05-27 06:55 UTC

Active-time accounting note: the usage-limit waiting gap remains excluded from
the twelve-hour floor. This checkpoint occurs at roughly eight active hours,
not twelve.

## Forcing Question

Does the only Wave21 residual/druggability candidate, `SQLE`, survive a
promotion-grade stress test when expression, residual specificity, foundation
model triage, real perturbation, LINCS/L1000, and prior-art evidence are
integrated?

## Result

No. `SQLE` is now closed as `NO_GO_SQLE_FAILFAST`.

Traceable output:

- Script: `scripts/v3_wave22_sqle_failfast.py`
- Output: `phases/v3/results/wave22_sqle_failfast/`
- Decision table: `phases/v3/results/wave22_sqle_failfast/sqle_decision.tsv`
- Summary: `phases/v3/results/wave22_sqle_failfast/summary.json`

Key numbers from the generated summary:

- Broad SQLE expression is positive in 4 diseases and negative in 0.
- Strict core-covariate residual survival is limited to 2 diseases:
  Crohn disease stromal and ulcerative colitis stromal.
- Non-IBD retained residual support is 1 disease.
- MS white-matter anchor is absent: `ms_wm_delta_log2 = -0.3408177110309154`,
  `ms_wm_p = 0.3307572199460259`.
- Geneformer triage is positive enough to inspect:
  3 support contexts and 1 strong context.
- Real perturbation alignment fails:
  `model_contradicted_by_gse162463_screen`, with MHC-II direction
  `mhcii_low_enrichment_contradictory`.
- LINCS compound metadata contains 5 known SQLE-inhibitor name rows, but those
  rows lack target/MOA annotations and SQLE-like compounds do not appear in the
  existing L1000 disease-signature reversal outputs.
- Prior-art/modality review remains `CONDITIONAL_NO`, with old antifungal,
  oncology, and metabolic SQLE inhibitor art and no V3-specific autoimmune
  delta.

## Track Beliefs

- Residual expression track: SQLE is a real IBD/stromal residual signal, not a
  cross-autoimmune target.
- Foundation-model track: Geneformer can flag SQLE as a possible state-shift
  token, but the real perturbation evidence contradicts target nomination. This
  is exactly the case where model triage must be subordinated to perturbation.
- Drug/perturbation track: existing SQLE chemical matter is not enough; without
  disease-signature reversal or target/MOA-annotated LINCS support, it is only
  a comparator.
- Prior-art track: SQLE is crowded and lacks a novel autoimmune-use delta.

## Decision

Close the residual/druggability rescue branch. The repeated failure pattern is
not "no druggable genes exist"; it is that residual expression survivors are
mostly tissue-repair, sterol, matrix, complement, or core inflammatory
machinery signals without causal direction.

## Next Forcing Question

Pivot away from residual-expression candidates and ask whether a different
evidence channel can identify an intervention point:

1. Does the cross-autoimmune module resolve into a metabolite-sensing or
   barrier-repair circuit with existing perturbational readouts rather than a
   single residual gene?
2. Does genetics-first negative-regulator biology (`PTPN2`, `SH2B3`,
   `TNFAIP3`, `CLEC16A`, `GPR65`) have an actionable modality when considered
   as restoration, not inhibition?
3. Are there treatment-response or clinical-trial subgroup data that identify a
   patient stratum where the shared lipid-lysosomal/APC module is predictive
   rather than merely descriptive?

The next wave should pursue these three routes in parallel and reject any route
that collapses back to expression-only evidence.
