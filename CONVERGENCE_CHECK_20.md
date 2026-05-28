# Convergence Check 20

Timestamp: 2026-05-27 11:55 UTC

## Inputs Since Check 19

- Wave58-M: `subagents_v3/wave58m_cxcr2_therapeutic_audit.md`.
- Wave58-N: `subagents_v3/wave58n_il7r_therapeutic_audit.md`.
- Wave58-O: `subagents_v3/wave58o_hostile_review_cxcr2_il7r.md`.
- Wave59 local audit:
  `results_v3/wave59_lysosomal_sphingolipid_model_reopener_audit/`.

## What Each Track Now Believes

Intervention-first receptor track:

- `CXCR2` is tractable and biologically real, but the evidence maps to
  neutrophil chemotaxis, psoriasis/IBD inflammatory composition, and
  already-published MS remyelination biology. It is not a novel
  lipid-lysosomal myeloid transition controller.
- `IL7R` is genetically real across autoimmunity, including MS, but the
  evidence maps to CD127/sIL7R adaptive-immune biology with direct clinical
  and patent prior art. It is not demonstrated to control the lipid-lysosomal
  myeloid module.

Lysosomal/sphingolipid model track:

- `CTSB`, `ASAH1`, `HEXB`, and `HEXA` explain some of the strongest
  Geneformer deletion signals, but they fail as therapeutic nodes because
  single-enzyme perturbation lacks safe/selective direction and does not align
  with MS genetics, local strict MS evidence, or real perturbation data.
- `GALC` has the best genetics/local breadth among this enzyme group, but no
  foundation-model support and no strict MS/perturbation/module-residual
  support.

## Agreement

- The cross-autoimmune lipid-lysosomal myeloid module remains plausible as a
  disease state.
- Directly modulating obvious single genes has repeatedly failed:
  housekeeping lysosomal enzymes fail directionality, while canonical immune
  receptors fail specificity and novelty.
- A promotable intervention probably has to sit at a state-transition,
  niche-signal, or response-stratification layer rather than at generic
  immune-cell trafficking/survival or organelle housekeeping.

## Disagreement / Open Tension

- Foundation-model token deletion can identify genes whose absence moves cells
  in embedding space, but it does not distinguish helpful state correction from
  harmful loss of core cellular function.
- Genetics tends to nominate canonical immune-risk genes and clinical targets,
  while local cell-state data nominates lysosomal/debris-handling genes. The
  overlap remains weak.

## Decision

Close `CXCR2`, `IL7R`, and direct lysosomal/sphingolipid enzyme modulation for
V3 therapeutic promotion.

Next forcing question:

Can a circuit-level or stratification-first analysis identify an upstream
controller of the lipid-lysosomal myeloid state that is druggable, less
prior-arted, and supported by real perturbation or response data across
multiple autoimmune diseases?

## Time Accounting Note

The user clarified that usage-limit gaps in the logs do not count as active
working time and that twelve active hours have not yet been reached. This
checkpoint therefore does not trigger `EXHAUSTION.md`; the session continues.
