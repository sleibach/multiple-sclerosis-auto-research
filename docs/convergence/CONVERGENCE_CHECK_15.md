# Convergence Check 15 - Perturbation/Repurposing Branch Closure

Timestamp: 2026-05-27 09:32 UTC

## Forcing Question

After the surfaceome/accessibility pivot failed, one perturbation-first item
remained unresolved: the Wave27 `PARK_EXTERNAL_TARGET_LOOKUP_ONLY` compound
`BRD-A72180425` / `K784-3188`. Could external target deconvolution turn that
single L1000 reversal hit into a tractable autoimmune intervention?

## New Evidence

Wave41 script:
`scripts/v3_wave41_l1000_external_unknown_deconvolution.py`

Outputs:
`phases/v3/results/wave41_l1000_external_unknown_deconvolution/`

Key result:

- `BRD-A72180425` resolves to PubChem CID `3689416` and ChEMBL
  `CHEMBL1472126`.
- It has one L1000 opposite-query hit only:
  `mif_cd74_receptor_state`.
- ChEMBL has 57 activity rows but zero mechanism records.
- L1000FWD DMOA lists known MOA and target(s) as `Unknown`.
- NCBI Bookshelf places `BRD-A72180425` in the ML162/RAS-selective-lethal
  probe SAR table, not in autoimmune therapeutic development.
- The structure contains a chloroacetamide-like electrophile motif.

Wave41 call:

- `NO_GO_CYTOTOXIC_PROBE_ANALOG`
- Promotion allowed: `False`

## Interpretation

The final unresolved L1000 item is not a hidden autoimmune drug candidate. It
is a cytotoxic/probe-family transcriptomic perturbation whose anti-signature is
more plausibly stress or cell-death biology than selective control of the
cross-autoimmune lipid-lysosomal myeloid module.

## Convergence State

The following routes now agree negatively:

- L1000 recurrence and unknown-compound deconvolution.
- Direct perturbation datasets.
- Treatment-response stratification.
- Surface/accessibility-first target rescue.
- Resolution/efferocytosis perturbation and CRISPR rescue.

The agreement is not that the lipid-lysosomal myeloid module is unimportant.
The agreement is narrower: the current candidate intervention handles are
either markers, crowded generic immunology, cytotoxic probes, inaccessible core
machinery, or not druggable in the needed direction.

## Next Forcing Question

The next branch should not continue fishing within L1000 or surface markers.
The remaining plausible route is genetics-first lipid biology that may not
manifest as differential expression. The best unresolved example is the
`FADS1/FADS2` desaturation locus: broad autoimmune mapped-gene recurrence,
lipid relevance, and direct enzyme druggability for `FADS1`, but weak local
cell-state evidence. This branch must be treated as a mechanistic/genetic
route, not an expression-surrogate route.
