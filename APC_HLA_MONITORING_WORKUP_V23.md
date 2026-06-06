# V23 Workup: APC/HLA-II Dynamic Treatment-Response Monitoring

## Executive Verdict

V23 strengthens but bounds the V22 monitoring lead.

The unbounded cross-therapy rule remains weak:

- primary locked V22 cohorts only: pooled AUC `0.547`, stratified bootstrap CI
  `0.337-0.743`; fixed/random-effects Hedges g `0.254`, CI `-0.437-0.945`.

The bounded immune-remodeling / cytokine-signaling domain is materially
stronger:

- dimethyl fumarate MS plus exact tofacitinib UC: pooled AUC `0.811`, CI
  `0.567-1.000`; pooled-subject Hedges g `1.191`, Welch p `0.0166`.
- after exact all-cell GSE253006 rescoring, primary locked plus exact UC gives
  AUC `0.656`, CI `0.489-0.808`; pooled-subject Hedges g `0.611`,
  Welch p `0.0499`.

Interpretation: the signal is not a universal treatment-response rule. It is a
provisional early-treatment monitoring signal for immune-remodeling /
cytokine-signaling contexts, with current support from small MS dimethyl
fumarate and UC tofacitinib cohorts. It fails or weakens in fingolimod/S1P
trafficking and psoriasis lesional adalimumab contexts.

No Tier 4 breakthrough is claimed: there are only two small primary
in-scope passes after exact UC cleanup, not three independent passes, and only
one MS DMT pass. No kill is claimed either.

## Action 1: Pooled Estimate

Outputs:

- `analysis/v23_apc_hla_monitoring/v23_pooled_locked_rule_summary.tsv`
- `analysis/v23_apc_hla_monitoring/v23_meta_analysis.json`

Key estimates:

| Analysis set | n | Cohorts | AUC | CI | Hedges g |
|---|---:|---|---:|---|---:|
| Primary locked V22 only | 34 | GSE235357; GSE250453; GSE85034_ADA | 0.547 | 0.337-0.743 | 0.180 |
| Primary locked plus exact UC all-cell | 43 | GSE235357; GSE250453; GSE253006_TOF_exact; GSE85034_ADA | 0.656 | 0.489-0.808 | 0.611 |
| Immune-remodeling/JAK-STAT bounded set | 19 | GSE235357; GSE253006_TOF_exact | 0.811 | 0.567-1.000 | 1.191 |

Fixed/random-effects meta-analysis of cohort-level Hedges g:

- primary locked only: g `0.254`, CI `-0.437-0.945`, I2 `0`.
- primary locked plus exact UC: fixed g `0.493`, CI `-0.142-1.129`; random g
  `0.515`, CI `-0.180-1.209`, I2 `0.152`.

## Action 2: Mechanism Specificity

Outputs:

- `analysis/v23_apc_hla_monitoring/v23_mechanism_specificity.tsv`
- `analysis/v23_apc_hla_monitoring/v23_mechanism_specificity_summary.tsv`
- `analysis/v23_apc_hla_monitoring/v23_mechanism_specificity_verdict.json`

Mechanism pattern:

- `GSE235357` dimethyl fumarate: immune redox/Nrf2 rebalancing, pass.
- `GSE253006_TOF_exact` tofacitinib: JAK-STAT cytokine signaling, pass.
- `GSE250453` fingolimod: lymphocyte trafficking/S1P, fail.
- `GSE85034_ADA` adalimumab in psoriasis lesional skin: TNF blockade in a
  non-mucosal tissue/outcome context, fail.

Verdict: mechanism-specificity is supported but small-n. The bounded domain is
plausible; the unbounded cross-therapy rule is not supported.

## Action 3: Exact GSE253006 Resolution

V22 disqualified the UC tofacitinib pass because it used a broader precomputed
IFN/APC module. V23 recomputed exact frozen V22 genes directly from raw 10x
matrices.

Output:

- `analysis/v23_apc_hla_monitoring/gse253006_exact_locked/gse253006_exact_validation_ledger.tsv`

Exact all-cell result:

- cohort: `GSE253006_TOF_exact`;
- n `9` (`5` responders, `4` nonresponders);
- feature: exact `-delta_IFN_APC`;
- AUC `0.95`, CI `0.70-1.00`;
- Hedges g `1.811`;
- Welch p `0.0162`;
- receptor control AUC `0.90`, below locked score by `0.05`;
- pass.

Caveat: all-cell pseudobulk remains compartment-unresolved, but it now uses the
exact frozen V22 genes.

## Action 4: Compartment And Mechanistic Grounding

V23 regenerated marker-derived compartments from raw GSE253006 matrices and
rescored exact frozen modules per compartment.

Output:

- `analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/gse253006_exact_compartment_validation.tsv`

Exact compartment results:

| Compartment | AUC | CI | Hedges g | Receptor AUC | Interpretation |
|---|---:|---|---:|---:|---|
| T-cell-like | 1.000 | 1.000-1.000 | 1.270 | 0.600 | Strongest specific compartment result. |
| B/plasma-like | 0.950 | 0.700-1.000 | 1.487 | 0.750 | Strong and receptor-specific. |
| Epithelial-like | 0.900 | 0.591-1.000 | 1.420 | 1.000 | Directional but receptor control is at least as strong; do not use as mechanism claim. |
| Myeloid/APC-like | 0.800 | 0.400-1.000 | 1.228 | 0.750 | Positive but weaker and wide CI. |
| Stromal/endothelial-like | 0.750 | 0.333-1.000 | 0.946 | 0.950 | Non-specific by receptor control; do not use as mechanism claim. |

Mechanistic conclusion:

- The UC tofacitinib signal is not restricted to myeloid/APC cells.
- The strongest specific signals are T-cell-like and B/plasma-like
  compartments.
- The most defensible biological statement is broader cytokine/JAK-STAT immune
  remodeling captured by IFN/APC/HLA genes, not an APC-only causal mechanism.
- This supports monitoring of therapy-induced immune-state movement, not
  pretreatment stratification and not a direct target nomination.

Precedence:

- The rule uses earliest post-treatment transcriptomic change. In GSE253006,
  most paired post samples are week 8; one responder's earliest available post
  sample is week 48, so that subject weakens strict early-precedence inference.
- In the MS DMT cohorts, the local metadata provide paired baseline/treated
  samples and clinical response labels, but V23 did not establish a precise
  clinical-response timing sequence sufficient for causal mediation.

## Action 5: Clinical Utility

The only supportable clinical use is early response monitoring.

Proposed use if validated:

- patient population: MS patients starting an immune-remodeling DMT, currently
  most plausibly dimethyl fumarate or a mechanistically similar therapy;
- sample: blood/PBMC RNA at baseline and a locked early on-treatment timepoint
  between week 1 and week 12;
- decision: continue therapy if the signed module movement is favorable, or
  consider early switch/escalation if not;
- expected benefit: reduce months-to-years spent on an ineffective DMT while
  irreversible MS activity accumulates;
- not supported: choosing therapy before first dose from baseline expression.

Prospective study:

- enroll at least `n=60` patients starting one mechanistically coherent DMT
  class, ideally DMF-like immune remodeling;
- lock the exact module, timepoint, normalization, and endpoint before outcome
  analysis;
- primary endpoint: 12-24 month relapse-free/NEDA or study-defined response;
- success: AUC `>= 0.70`, lower CI `> 0.55`, Hedges g `>= 0.50`, receptor
  control not better by AUC `>= 0.10`;
- stop-loss: AUC `< 0.55` or Hedges g `< 0.20`.

## Action 6: Successor Rule Decision

Do not lock `LOCKED_RULE_V23.md` in this session.

Reason:

- A bounded successor rule is scientifically plausible:
  immune-remodeling/JAK-STAT contexts only, not S1P trafficking or all
  cytokine blockade contexts.
- But the bounded rule is motivated by all currently reachable successful data:
  DMF and exact UC tofacitinib.
- There is no unused held-out cohort left in the current workspace to test a
  successor lock honestly.

Therefore a V23 successor lock would be pre-registration theater unless a fresh
held-out cohort is acquired first.

## Current Status

V23 advances the lead from "mixed provisional" to:

> A bounded, small-n, early-treatment monitoring hypothesis: favorable early
> IFN/APC downshift or HLA-II-vs-IFN/APC remodeling tracks response in
> immune-remodeling/JAK-STAT contexts, but does not generalize across all
> therapies or compartments.

This is actionable as a prospective biomarker study design, not as a validated
clinical rule.

