# Convergence Check 101 - External Human Interface Perturbation

Timestamp: 2026-05-28 09:08 CEST

## What Changed

Wave151 identified a missing direct perturbation context. Wave152 filled part
of that gap with four verified public human interface-cell perturbation
datasets:

- `GSE190634`: primary human colonoid cytokine response.
- `GSE217552`: primary adult human epidermal keratinocyte TNF/IL17 activation
  and treatment rescue.
- `GSE200309`: human iPSC-derived intestinal epithelial SCFA perturbation.
- `GSE237845`: human colonic fibroblast TWEAK/TNFSF12 perturbation.

## Agreement

The broadest recurrent human interface-cell signal is still inflammatory
chemokine/adhesion biology:

- `epithelial_chemokine_entry` is induced in all four analyzed datasets.
- `endothelial_entry` is induced in three analyzed datasets.

This agrees with the earlier architecture/barrier track that tissue-interface
programs recur across autoimmune-like contexts.

## Blocking Point

No module passes the stricter therapeutic route gate. The missing piece is not
induction; it is a selective perturbation that reverses the induced module
without collapsing into generic anti-inflammatory or stress biology.

## Next Forcing Question

Can a human fibroblast genetic perturbation dataset identify a controller of
the recurrent chemokine/adhesion/interface program?

`GSE129488` is the next priority because its design includes TNF/IL17 induction
and siRNA perturbations in human synovial fibroblasts. The immediate task is to
resolve the superseries into accessible subseries or supplementary expression
matrices.
