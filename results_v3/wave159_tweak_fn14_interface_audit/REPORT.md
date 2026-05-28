# Wave159 TWEAK/Fn14 Interface Audit

Branch call: `NO_TWEAK_FN14_ROUTE_PROMOTION`.

## Result

This wave does not promote TWEAK/Fn14 or a downstream non-ELR effector as the V3 finding.

## Basis

- Dataset: GSE237845, human CCD-18Co colonic fibroblasts, TWEAK/TNFSF12 24h vs vehicle.
- Genes tested: `18711`.
- FDR10 upregulated genes: `725`.
- Nominal non-ELR upregulated genes: `2096`.
- Candidate gate requires perturbation response, MS anchor, cross-disease anchor, and reachable intervention architecture.

## Interpretation

GSE237845 provides real human fibroblast TWEAK perturbation data, but local cross-disease/MS/genetic/reachability gates do not yet promote TNFSF12/TNFRSF12A or immediate non-ELR downstream genes.
